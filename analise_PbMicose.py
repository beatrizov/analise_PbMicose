import pandas as pd
import numpy as np
import warnings
from sklearn.metrics import cohen_kappa_score
from statsmodels.stats.inter_rater import aggregate_raters, fleiss_kappa
from collections import Counter

# Ignora avisos futuros
warnings.simplefilter(action='ignore', category=FutureWarning)

# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS

# Coloque aqui o nome exato do seu novo arquivo
nome_arquivo = 'Primeiros_Diagnosticos_Consolidados.csv'
df = pd.read_csv(nome_arquivo)

# Preenche os "Casos" em branco com o nome da linha de cima (Ffill)
df['Caso'] = df['Caso'].ffill()

# Remove linhas inteiramente vazias ou que não possuem um modelo associado
df = df.dropna(subset=['LLM'])

# Limpa espaços em branco ocultos nas pontas das palavras
df['Caso'] = df['Caso'].astype(str).str.strip()
df['LLM'] = df['LLM'].astype(str).str.strip()

# 2. PADRONIZAÇÃO FINAL DAS CATEGORIAS
# O Fleiss e Cohen exigem que os nomes das doenças sejam idênticos.
def padronizar_diagnostico(texto):
    if pd.isna(texto):
        return "Indeterminado/Sem resposta"
    
    texto = str(texto).lower()
    
    if "coccidio" in texto: return "Coccidioidomicose"
    if "crypto" in texto or "cripto" in texto: return "Criptococose"
    if "candida" in texto or "levedura" in texto: return "Candidíase"
    if "aspergil" in texto: return "Aspergilose"
    if "paracoccidio" in texto: return "Paracoccidioidomicose"
    if "histoplas" in texto: return "Histoplasmose"
    if "blastomy" in texto or "blastomi" in texto: return "Blastomicose"
    if "pneumocystis" in texto: return "Pneumocistose"
    if "pensamento" in texto: return "Erro/Indeterminado" # Para respostas onde a LLM travou
    
    return "Outro/Indeterminado"

df['Diag_Padrao'] = df['Primeiro_Diagnostico'].apply(padronizar_diagnostico)

# 3. REORGANIZAÇÃO PARA AS MÉTRICAS (DE FORMATO LONGO PARA LARGO)
# Cria as "Rodadas" numerando as respostas (1, 2, 3) para cada Caso e LLM
df['Rodada'] = df.groupby(['Caso', 'LLM']).cumcount() + 1

# Transforma a tabela para que as rodadas fiquem lado a lado nas colunas
df_rodadas = df.pivot_table(
    index=['Caso', 'LLM'], 
    columns='Rodada', 
    values='Diag_Padrao', 
    aggfunc='first'
).reset_index()

# Preenche valores faltantes caso alguma rodada tenha sido perdida
df_rodadas = df_rodadas.fillna("Indeterminado/Sem resposta")

# Identifica quais colunas representam as rodadas numéricas (1, 2, 3)
colunas_rodadas = [col for col in df_rodadas.columns if isinstance(col, int)]

# 4. REPRODUTIBILIDADE (ACORDO INTRA-LLM) - KAPPA DE FLEISS
print("--- AVALIAÇÃO DE REPRODUTIBILIDADE (INTRA-LLM) ---")

llms = df_rodadas['LLM'].unique()

for llm in llms:
    df_llm = df_rodadas[df_rodadas['LLM'] == llm].copy()
    
    if len(df_llm) == 0:
        continue
        
    tabela_respostas = df_llm[colunas_rodadas].values
    
    formatted_data, categorias = aggregate_raters(tabela_respostas)
    kappa_f = fleiss_kappa(formatted_data)
    print(f"Modelo: {llm} | Kappa de Fleiss ({len(colunas_rodadas)} rodadas): {kappa_f:.4f}")

print("\n")

# 5. CONSISTÊNCIA (ACORDO INTER-LLM) - KAPPA DE COHEN
print("--- AVALIAÇÃO DE CONSISTÊNCIA (INTER-LLM) ---")

# Define o diagnóstico final de cada LLM como a moda (voto da maioria) das rodadas
def voto_maioria(linha):
    votos = [linha[c] for c in colunas_rodadas]
    return Counter(votos).most_common(1)[0][0]

df_rodadas['Diagnostico_Final'] = df_rodadas.apply(voto_maioria, axis=1)

# Reestrutura novamente para cruzar Modelo A vs Modelo B
df_pivot_cohen = df_rodadas.pivot_table(
    index='Caso', 
    columns='LLM', 
    values='Diagnostico_Final', 
    aggfunc='first'
).dropna()

modelos_presentes = df_pivot_cohen.columns.tolist()

# Calcula o Kappa de Cohen comparando os modelos em pares
for i in range(len(modelos_presentes)):
    for j in range(i + 1, len(modelos_presentes)):
        modelo_1 = modelos_presentes[i]
        modelo_2 = modelos_presentes[j]
        
        kappa_c = cohen_kappa_score(df_pivot_cohen[modelo_1], df_pivot_cohen[modelo_2])
        
        print(f"Acordo entre {modelo_1} e {modelo_2} | Kappa de Cohen: {kappa_c:.4f}")