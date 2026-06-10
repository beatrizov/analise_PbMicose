# Análise de Concordância de LLMs em Diagnósticos Patológicos 🔬🤖

Este repositório contém o script em Python desenvolvido para o meu Trabalho de Conclusão de Curso (TCC) na Universidade de São Paulo (USP). O objetivo do projeto é avaliar a precisão, reprodutibilidade e consistência de Modelos de Linguagem de Grande Escala (LLMs) — como **GPT, Gemini e Copilot** — na formulação de hipóteses diagnósticas de micoses (ex: *Paracoccidioidomicose, Coccidioidomicose, Aspergilose*, entre outras) a partir da análise de imagens histopatológicas.

## 🎯 Metodologia de Avaliação

O script realiza a leitura de dados extraídos dos prompts gerados pelas LLMs e aplica métricas estatísticas de concordância:

1. **Reprodutibilidade (Acordo Intra-LLM) - *Kappa de Fleiss*:** Avalia a estabilidade das respostas de cada LLM. Cada modelo avalia o mesmo conjunto de dados (casos) três vezes em sessões independentes (Rodadas 1, 2 e 3). O cálculo mede o quanto o modelo concorda consigo mesmo ao longo das repetições.

2. **Consistência (Acordo Inter-LLM) - *Kappa de Cohen*:**
   Avalia a concordância entre os diagnósticos finais sugeridos por diferentes modelos (ex: GPT vs. Gemini, GPT vs. Copilot). O diagnóstico final de cada modelo é definido pelo voto da maioria (moda) entre as suas rodadas.

## 🛠️ Tecnologias e Bibliotecas Utilizadas

* **Python 3.x**
* **Pandas & NumPy** (Manipulação e estruturação de dados em formato longo e largo)
* **Statsmodels** (Cálculo do Kappa de Fleiss)
* **Scikit-Learn** (Cálculo do Kappa de Cohen)

## 📂 Estrutura de Dados Esperada

O script processa planilhas consolidadas (`.csv`) contendo a primeira hipótese diagnóstica de cada modelo para cada caso. A estrutura esperada é no formato longo (empilhado):

| Caso | LLM | Primeiro_Diagnostico |
| :--- | :--- | :--- |
| Paciente_01 | GPT | Paracoccidioides spp. |
| Paciente_01 | Gemini | Coccidioidomycosis |
| Paciente_01 | Copilot | Candida spp. |
*(Obs: Os nomes de pacientes e casos originais foram anonimizados para proteção de dados médicos e ética em pesquisa).*

## 🚀 Como executar o projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/beatrizov/analise_PbMicose.git](https://github.com/beatrizov/analisePbMicose.git)
   cd NOME_DO_REPOSITORIO

```

2. **Instale as dependências:**
É recomendado o uso de um ambiente virtual (venv).
```bash
pip install pandas numpy scikit-learn statsmodels

```


3. **Execute o script de análise:**
Certifique-se de que a planilha `.csv` está no mesmo diretório do script ou ajuste o caminho no código.
```bash
python analise_PbMicose.py

```



## 📊 Interpretação dos Resultados

O script imprimirá no terminal os valores de Kappa. Segundo a literatura clássica (Landis & Koch, 1977), a interpretação obedece à seguinte escala:

* **< 0,00:** Pior que o acaso
* **0,00 - 0,20:** Concordância leve
* **0,21 - 0,40:** Concordância razoável
* **0,41 - 0,60:** Concordância moderada
* **0,61 - 0,80:** Concordância substancial
* **0,81 - 1,00:** Concordância quase perfeita

---
