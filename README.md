# Decision Tree Classifier - Diabetes Prediction

### Descrição
Este projeto implementa a construção e avaliação de uma árvore de decisão utilizando diferentes funções de divisão: Information Gain, Gain Ratio e Gini. O usuário pode escolher qual métrica utilizar para construir a árvore, visualizar o grafo gerado e conferir as métricas de desempenho do modelo.

### Base de Dados

Este projeto utiliza a base de dados [Pima Indians Diabetes Database](https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database), composta por informações clínicas de pacientes do grupo indígena Pima, com o objetivo de prever a ocorrência de diabetes. O conjunto possui 768 registros e 8 atributos, incluindo número de gestações, glicose, pressão arterial, espessura da pele, insulina, índice de massa corporal (IMC), função pedigree do diabetes e idade, além da variável alvo indicando a presença ou ausência de diabetes.

<hr>

### Requisitos
 - Python 3.x
 - pip
 - Graphviz (instalação necessária para visualização da árvore de decisão)

### Guia de compilação e execução
1. Clone o repositório:
```git clone https://github.com/Samuel-Salvador/Decision-Tree-Diabetes.git```


2. Navegue até o diretório do repositório clonado:
```cd Decision-Tree-Diabetes```


3. Crie um ambiente virtual (opcional, mas recomendado):
```python -m venv venv```


4. Ative o ambiente virtual:

   - No Windows:
   ```venv\Scripts\activate```
   
   - No Linux/Mac:
   ```source venv/bin/activate```


5. Instale as dependências Python:
```pip install -r requirements.txt```


6. Instalação do Graphviz:

     - Baixe o Graphviz pelo site oficial: https://graphviz.gitlab.io/download/.
     - Durante a instalação, certifique-se de adicionar o Graphviz ao PATH do sistema.


8. Execute o script principal: 
```python main.py```

<hr>

### Saída
Após a execução do script, o usuário poderá escolher a métrica de divisão da árvore de decisão. O programa irá gerar um grafo da árvore e exibir as métricas de desempenho do modelo, incluindo acurácia, precisão, recall e F1-score.



