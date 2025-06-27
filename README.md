# lancamentos_seguros

# Gerador de Lançamentos Contábeis de Seguro

Este projeto tem como objetivo automatizar e agilizar um processo repetitivo do meu trabalho no setor contábil. Frequentemente, preciso lançar as informações de apólices de seguro, como o valor do seguro, IOF, juros e outras despesas, em planilhas, para posterior importação em sistemas contábeis (como o Domínio). Como esse processo envolve muitas etapas repetitivas, decidi usar o ChatGPT para criar uma ferramenta que facilitasse essa tarefa.

### **Objetivo do Projeto**

Este sistema foi desenvolvido para gerar lançamentos contábeis de forma rápida e eficiente, através de uma interface simples. A entrada de dados é feita pelo usuário, que informa as informações da apólice de seguro, e a saída do sistema é uma **planilha CSV**, que contém os lançamentos contábeis prontos para serem importados no sistema contábil.

### **Uso do ChatGPT**

A ideia de automatizar essa tarefa surgiu após algumas interações com o ChatGPT. Usei a versão gratuita do ChatGPT para agilizar o desenvolvimento, já que o processo não envolveu dados sensíveis de clientes. Graças ao poder da IA, consegui criar rapidamente um código funcional que reduz bastante o tempo gasto com tarefas manuais e repetitivas.

### **Funcionalidade**

Atualmente, o sistema gera uma planilha CSV com os lançamentos contábeis a partir dos dados fornecidos pelo usuário. A planilha contém as seguintes informações:

* **Valor do Seguro**
* **Valor do IOF**
* **Valor de Juros ou Outras Despesas**
* **Contas de Débito e Crédito**
* **Históricos de lançamento formatados de acordo com os dados da apólice**

Esses dados são inseridos em uma planilha que pode ser convertida para o formato necessário para importação no sistema Domínio.

### **Futuro do Projeto**

Ainda existem melhorias a serem feitas, especialmente no que diz respeito à usabilidade da interface e a automação do processo de importação diretamente no sistema Domínio. No futuro, pretendo implementar uma versão mais robusta com outras funcionalidades que possam ser aplicadas diretamente em sistemas de contabilidade, para reduzir ainda mais a necessidade de intervenção manual.

---

**Tecnologias utilizadas**:

* Python
* Streamlit (para a interface)
* Pandas, csv
* ChatGPT (para o desenvolvimento rápido do código)

**Como rodar**:

1. Clone o repositório.
2. Instale as dependências necessárias com `pip install -r requirements.txt`.
3. Execute o script com `streamlit run app.py`.
