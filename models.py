import math
import pydot
from copy import deepcopy
from typing import List
import networkx as nx
from ModelData import ModelData
from Person import Person
from data_set import Data
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

class Modelo:
    arvore = {
        'graph': pydot.Dot(graph_type='digraph'),
        'qnt_nodes': 0
              }
    dados = {'classificacao_real': [],
             'classificacao_modelo': []}

    @classmethod
    def imprimir_metricas(cls):
        cls.dados['classificacao_real'] = [int(pessoa.outcome) for pessoa in Data.get_lista_de_pessoas()]

        accuracy = accuracy_score(cls.dados['classificacao_real'], cls.dados['classificacao_modelo'])
        precision = precision_score(cls.dados['classificacao_real'], cls.dados['classificacao_modelo'], zero_division=0)
        recall = recall_score(cls.dados['classificacao_real'], cls.dados['classificacao_modelo'], zero_division=0)
        f1 = f1_score(cls.dados['classificacao_real'], cls.dados['classificacao_modelo'], zero_division=0)
        matriz_confusao = confusion_matrix(cls.dados['classificacao_real'], cls.dados['classificacao_modelo'])

        print(f"Acurácia: {round(accuracy * 100, 2)}%")
        print(f"Precisão: {round(precision * 100, 2)}%")
        print(f"Recall: {round(recall * 100, 2)}%")
        print(f"F1-Score: {round(f1 * 100, 2)}%")
        print(f"Matriz de Confusão:\n", matriz_confusao)

    @classmethod
    def testar_modelo(cls):

        global lista_arestas_node_atual
        lista_teste = Data.get_lista_de_pessoas()

        grafo = nx.nx_pydot.from_pydot(cls.arvore['graph'])
        nodes_do_grafo = list(grafo.nodes())

        classificacao_correta = 0

        for pessoa in lista_teste:
            indice_node_atual = 0
            flag = False
            while True:

                if not flag:
                    lista_arestas_node_atual = list(grafo.out_edges(nodes_do_grafo[indice_node_atual], data=True))
                elif flag:
                    lista_arestas_node_atual = list(grafo.out_edges(nodes_do_grafo[indice_node_atual], data=True))

                flag = True
                if len(lista_arestas_node_atual) == 0:

                    if grafo.nodes[str(indice_node_atual)].get('label') == "Sem Diabetes":
                        cls.dados['classificacao_modelo'].append(0)
                        if pessoa.outcome == '0':
                            classificacao_correta += 1

                    elif grafo.nodes[str(indice_node_atual)].get('label') == "Com Diabetes":
                        cls.dados['classificacao_modelo'].append(1)
                        if pessoa.outcome == '1':
                            classificacao_correta += 1
                    break

                valor_do_atr_da_pessoa = getattr(pessoa,grafo.nodes[str(indice_node_atual)].get('label'))

                classificacao_do_atr_da_pessoa = ModelData.get_var_from_values_and_atr(grafo.nodes[str(indice_node_atual)].get('label'),valor_do_atr_da_pessoa)

                for aresta in lista_arestas_node_atual:
                    if aresta[2]['label'] == classificacao_do_atr_da_pessoa:

                        indice_node_atual = int(aresta[1])

        print(f'{classificacao_correta} de {len(lista_teste)} classificados corretamente, equivalente a {round((classificacao_correta/ len(lista_teste)*100),2)}%')

    @classmethod
    def criar_no_da_arvore(cls, no_pai: pydot.Node, var: str, atr_checados: List[str], lista_pessoas: List[Person], tipo: str):
        model_data = None

        if len(lista_pessoas) == 0:
            model_data = cls.preencher_dicionario_completo(Data.get_lista_treinamento())

        else:
            model_data = cls.preencher_dicionario_completo(lista_pessoas)

        atr = cls.checar_maior_funcao(model_data, atr_checados, tipo)

        if atr == '':
            return
        atributos_checados = atr_checados + [atr]

        novo_no = pydot.Node( str( cls.arvore['qnt_nodes'] ), label= f'{atr}')
        cls.arvore['qnt_nodes'] += 1
        cls.arvore['graph'].add_node(novo_no)

        if (no_pai is not None) and (var is not None):
          cls.arvore['graph'].add_edge(pydot.Edge(no_pai, novo_no, label=f'{var}'))

        for variavel in model_data.dados[atr].keys():

            if variavel.startswith('qnt'):
                break

            if model_data.dados[atr][variavel]['qnt_diabeticos'] == 0:
                no_folha = pydot.Node(str(cls.arvore['qnt_nodes']), label='Sem Diabetes')
                cls.arvore['qnt_nodes'] += 1
                cls.arvore['graph'].add_node(no_folha)
                cls.arvore['graph'].add_edge(pydot.Edge( novo_no, no_folha, label=f'{variavel}'))
                continue

            elif len(model_data.dados[atr][variavel]['lista_pessoas']) == model_data.dados[atr][variavel]['qnt_diabeticos']:
                no_folha = pydot.Node(str(cls.arvore['qnt_nodes']), label="Com Diabetes")
                cls.arvore['qnt_nodes'] += 1
                cls.arvore['graph'].add_node(no_folha)
                cls.arvore['graph'].add_edge(pydot.Edge(novo_no, no_folha, label=f'{variavel}'))
                continue

            elif len(atributos_checados) == 8:
                porcentagem_diabeticos = model_data.dados[atr][variavel]['qnt_diabeticos'] / len(model_data.dados[atr][variavel]['lista_pessoas'])

                if porcentagem_diabeticos <= 0.50 :
                    no_folha = pydot.Node( str( cls.arvore['qnt_nodes'] ),label="Sem Diabetes")
                    cls.arvore['qnt_nodes'] += 1
                    cls.arvore['graph'].add_node(no_folha)
                    cls.arvore['graph'].add_edge(pydot.Edge(novo_no, no_folha, label=f'{variavel}'))
                    continue
                elif porcentagem_diabeticos > 0.50:
                    no_folha = pydot.Node( str( cls.arvore['qnt_nodes'] ),label="Com Diabetes")
                    cls.arvore['qnt_nodes'] += 1
                    cls.arvore['graph'].add_node(no_folha)
                    cls.arvore['graph'].add_edge(pydot.Edge(novo_no, no_folha, label=f'{variavel}'))
                    continue

            else:
                novo_model_data = cls.preencher_dicionario_completo(model_data.dados[atr][variavel]['lista_pessoas'])
                cls.criar_no_da_arvore(novo_no, variavel, atributos_checados, novo_model_data.dados[atr][variavel]['lista_pessoas'], tipo)


    # ATÉ Aqui tá certo! tem que ver pra cima agora
    @classmethod
    def checar_maior_funcao(cls, model_data: ModelData, atributos_checados: List[str], tipo: str) -> str:
        maior_num_funcao = -999
        atributo_da_maior_funcao = ''

        lista_de_atributos = deepcopy(list(model_data.dados.keys()))
        for atributo in atributos_checados:
            try:
                lista_de_atributos.remove(atributo)
            except ValueError:
                continue

        for atributo in lista_de_atributos:
            funcao_calculada = 0.0
            if tipo == 'ig':
                funcao_calculada = cls.calcular_ig(model_data, atributo)
            elif tipo == 'gr':
                funcao_calculada = cls.calcular_gain_ratio(model_data, atributo)
            elif tipo == 'gini':
                funcao_calculada = cls.calcular_gini(model_data, atributo)

            if funcao_calculada > maior_num_funcao:

                maior_num_funcao = funcao_calculada
                atributo_da_maior_funcao = atributo

        return atributo_da_maior_funcao

    @classmethod
    def calcular_ig(cls, model_data: ModelData, atributo: str):

        entropia_atributo = cls.calcular_entropia_atr(model_data,atributo)
        entropia_conjunto = cls.calcular_entropia_conjunto(model_data,atributo)

        return entropia_conjunto - entropia_atributo

    @classmethod
    def calcular_gini(cls, model_data: ModelData, atributo: str):

        gini_atr = 0

        for chave in model_data.dados.get(atributo).keys():
            if chave.startswith("qnt"):
                break

            probabilidade_var_com_diabetes = cls.calculo_probabilidade(model_data, atributo, chave, tipo='var')
            probabilidade_var_sem_diabetes = 1 - probabilidade_var_com_diabetes

            gini_var = 1 - (probabilidade_var_com_diabetes ** 2) - (probabilidade_var_sem_diabetes ** 2)

            gini_atr += cls.calculo_probabilidade(model_data, atributo, chave, tipo='atr') * gini_var

        return gini_atr

    @classmethod
    def calcular_gain_ratio(cls, model_data: ModelData, atributo: str):
        entropia_gain_ratio = 0

        for chave in model_data.dados.get(atributo).keys():
            if chave.startswith("qnt"):
                break
            probabilidade_atr = cls.calculo_probabilidade(model_data,atributo, chave, tipo='atr')

            if not probabilidade_atr:
                return 0.0

            entropia_gain_ratio -= probabilidade_atr * math.log(probabilidade_atr,2)

        return cls.calcular_ig(model_data, atributo) / entropia_gain_ratio

    @classmethod
    def calcular_entropia_conjunto(cls, model_data: ModelData,atributo: str):

        entropia_do_conjunto = cls.calcular_entropia(cls.calculo_probabilidade(model_data, atributo, tipo='conj'))

        return entropia_do_conjunto

    @classmethod
    def calcular_entropia_atr(cls, model_data: ModelData, atributo: str) -> float:
        entropia_atr = 0.0

        for chave in model_data.dados.get(atributo).keys():
            if chave.startswith("qnt"):
                break

            entropia_atr += cls.calculo_probabilidade(model_data,atributo, chave, 'atr') * cls.calcular_entropia(cls.calculo_probabilidade(model_data,atributo, chave, tipo='var'))

        return entropia_atr

    @classmethod
    def calcular_entropia(cls, probabilidade_diabete: float) -> float:
        probabilidade_sem_diabete = 1.0 - probabilidade_diabete

        if not probabilidade_diabete or not probabilidade_sem_diabete:
            return 0.0

        entropia = - probabilidade_diabete * math.log(probabilidade_diabete,2) - probabilidade_sem_diabete * math.log(probabilidade_sem_diabete, 2)

        return entropia

    @classmethod
    def calculo_probabilidade(cls, model_data: ModelData, atributo: str, nome_var: str = None, tipo: str = None) -> float:
        probabilidade = 0.0

        if tipo == 'var':
            if not nome_var:
                raise AttributeError("Para o tipo de probabilidade 'var' é necessário o parâmetro 'nome_var'")
            qnt_pessoas_com_diabetes = model_data.dados[atributo][nome_var]['qnt_diabeticos']
            total_pessoas = len(model_data.dados[atributo][nome_var]['lista_pessoas'])

            if total_pessoas == 0:
                return 0.0

            probabilidade = qnt_pessoas_com_diabetes / total_pessoas

        elif tipo == 'atr':
            if not nome_var:
                raise AttributeError("Para o tipo de probabilidade 'atr' é necessário o parâmetro 'nome_var'")
            qnt_pessoas_da_var = len(model_data.dados[atributo][nome_var]['lista_pessoas'])
            total_pessoas_atr = model_data.dados[atributo]['qnt_pessoas']
            probabilidade = qnt_pessoas_da_var / total_pessoas_atr

        elif tipo == 'conj':
            qnt_pessoas_com_diabetes = model_data.dados[atributo]['qnt_diabeticos_atr']
            total_pessoas = model_data.dados[atributo]['qnt_pessoas']
            probabilidade = qnt_pessoas_com_diabetes / total_pessoas
        else:
            raise AttributeError("Tipo de probabilidade inválido ou não selecionado!")

        return probabilidade

    @classmethod
    def preencher_dicionario_completo(cls, lista_de_pessoas: List[Person]):
        model_data = ModelData()

        for atributo in model_data.dados.keys():
            cls.preencher_atr_do_dicionario(atributo, lista_de_pessoas, model_data)

        return model_data

    @classmethod
    def preencher_atr_do_dicionario(cls, atributo: str, lista_de_pessoas: List[Person], model_data : ModelData):
        quantidade_diabeticos = 0

        if atributo == '_pregnancies':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_pregnancies', 'normal', lista_de_pessoas, model_data, menor_que=4)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_pregnancies', 'elevado', lista_de_pessoas, model_data, maior_que=4)

        elif atributo == '_glucose':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_glucose', 'baixo', lista_de_pessoas, model_data, menor_que=65)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_glucose', 'normal', lista_de_pessoas, model_data, maior_que=65, menor_que=100)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_glucose', 'alto', lista_de_pessoas, model_data, maior_que=100, menor_que=125)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_glucose', 'altissimo', lista_de_pessoas, model_data, maior_que=125)

        elif atributo == '_blood_pressure':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_blood_pressure', 'baixo', lista_de_pessoas, model_data, menor_que=50)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_blood_pressure', 'normal', lista_de_pessoas, model_data, maior_que=50, menor_que=80)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_blood_pressure', 'alto', lista_de_pessoas, model_data, maior_que=80)

        elif atributo == '_skin_thickness':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_skin_thickness', 'normal', lista_de_pessoas, model_data, menor_que=20)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_skin_thickness', 'elevado', lista_de_pessoas, model_data, maior_que=20)

        elif atributo == '_insulin':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_insulin', 'normal', lista_de_pessoas, model_data, menor_que=140)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_insulin', 'elevado', lista_de_pessoas, model_data, maior_que=140, menor_que=200)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_insulin', 'altissimo', lista_de_pessoas, model_data, maior_que=200)

        elif atributo == '_bmi':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_bmi', 'normal', lista_de_pessoas, model_data, menor_que=25)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_bmi', 'sobrepeso', lista_de_pessoas, model_data, maior_que=25, menor_que=30)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_bmi', 'obesidade', lista_de_pessoas, model_data, maior_que=30)

        elif atributo == '_diabetes_pedigree_function':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_diabetes_pedigree_function', 'baixo', lista_de_pessoas, model_data,menor_que=0.5)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_diabetes_pedigree_function', 'moderado', lista_de_pessoas, model_data,maior_que=0.5, menor_que=1.0)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_diabetes_pedigree_function', 'alto', lista_de_pessoas, model_data,maior_que=1.0)

        elif atributo == '_age':
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_age', 'jovem', lista_de_pessoas, model_data,menor_que=35)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_age', 'adulto', lista_de_pessoas, model_data,maior_que=35, menor_que=55)
            quantidade_diabeticos += cls.preencher_dicionario_de_dentro('_age', 'idoso', lista_de_pessoas, model_data,maior_que=55)

        else:
            raise AttributeError('Atributo não está presente na classe Person')

        model_data.dados[atributo]['qnt_diabeticos_atr'] = quantidade_diabeticos

    @classmethod
    def preencher_dicionario_de_dentro(cls, atributo: str, nome_var: str, lista_pessoas: List[Person], model_data: ModelData, menor_que = None, maior_que = None) -> int:
        pessoas_com_diabetes = 0

        if menor_que and maior_que:
            for pessoa in lista_pessoas:
                if maior_que <= float(getattr(pessoa,atributo)) < menor_que:
                    model_data.dados[atributo][nome_var]['lista_pessoas'].append(pessoa)

                    if pessoa.outcome == '1':
                        pessoas_com_diabetes += 1

            model_data.dados[atributo][nome_var]['qnt_diabeticos'] = pessoas_com_diabetes
            model_data.dados[atributo]['qnt_pessoas'] += len(model_data.dados[atributo][nome_var]['lista_pessoas'])

        elif maior_que:
            for pessoa in lista_pessoas:
                if maior_que <= float(getattr(pessoa,atributo)):
                    model_data.dados[atributo][nome_var]['lista_pessoas'].append(pessoa)

                    if pessoa.outcome == '1':
                        pessoas_com_diabetes += 1

            model_data.dados[atributo][nome_var]['qnt_diabeticos'] = pessoas_com_diabetes
            model_data.dados[atributo]['qnt_pessoas'] += len(model_data.dados[atributo][nome_var]['lista_pessoas'])

        elif menor_que:
            for pessoa in lista_pessoas:
                if  float(getattr(pessoa,atributo)) < menor_que:
                    model_data.dados[atributo][nome_var]['lista_pessoas'].append(pessoa)

                    if pessoa.outcome == '1':
                        pessoas_com_diabetes += 1

            model_data.dados[atributo][nome_var]['qnt_diabeticos'] = pessoas_com_diabetes
            model_data.dados[atributo]['qnt_pessoas'] += len(model_data.dados[atributo][nome_var]['lista_pessoas'])

        else:
            raise AttributeError('Use menor_que e/ou maior_que como atributo')

        return pessoas_com_diabetes

