from data_set import Data
import models

Data.coletar_dados_csv()
Data.preencher_dado_ausente()
Data.separar_dados()

print("Qual a funcao que quer usar para construção da árvore?")
print("1 - Information Gain")
print("2 - Gain Ratio")
print("3 - Gini\n")

entrada = 0
tipo = 0

while entrada not in ('1', '2', '3'):

    entrada = input("Digite '1', '2' ou '3': ")
if entrada == '1':
    tipo = 'ig'
elif entrada == '2':
    tipo = 'gr'
elif entrada == '3':
    tipo = 'gini'

models.Modelo.criar_no_da_arvore(None, None, list(),list(), tipo)
models.Modelo.arvore['graph'].write_png("graph.png")
models.Modelo.testar_modelo()
models.Modelo.imprimir_metricas()
