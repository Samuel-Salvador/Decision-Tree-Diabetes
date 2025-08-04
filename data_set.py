import csv
from Person import Person
from pathlib import Path
from typing import List
from statistics import median

CAMINHO_ARQUIVO = Path(__file__).parent / 'diabetes.csv'

class Data:

    __perfil = 'teste'

    _lista_de_pessoas: List[Person] = []

    _lista_treinamento: List[Person] = []
    _lista_teste: List[Person] = []

    PORCENTAGEM_DADOS_TESTE = 0.40

    @classmethod
    def set_perfil(cls, perfil: str):
        cls.__perfil = perfil

    @classmethod
    def get_perfil(cls):
        return cls.__perfil

    @classmethod
    def get_lista_de_pessoas(cls):
        if cls.get_perfil() == 'treinamento':
            return cls._lista_treinamento

        elif cls.get_perfil() == 'teste':
            return cls._lista_teste

        elif cls.get_perfil() == 'tudo':
            return cls._lista_de_pessoas

        raise Exception('Perfil atual inválido. Mude o perfil para: "teste" ou "treinamento"')

    @classmethod
    def get_lista_treinamento(cls):
        return cls._lista_treinamento

    @classmethod
    def get_lista_teste(cls):
        return cls._lista_teste

    @classmethod
    def coletar_dados_csv(cls):
        with open(CAMINHO_ARQUIVO, 'r') as my_file:
            leitor = csv.reader(my_file)
            next(leitor)

            for linha in leitor:
                pessoa = Person(linha)
                cls._lista_de_pessoas.append(pessoa)

    @classmethod
    def preencher_dado_ausente(cls):

        for pessoa in cls._lista_de_pessoas:

            while True:

                dado_checado = cls.checar_dado(pessoa)
                lista_dados_validos: List[Person] = []

                if dado_checado == -1:
                    break

                elif dado_checado == 1:
                    for person in cls._lista_de_pessoas:
                        if person.glucose != '0':
                            lista_dados_validos.append(person)

                    lista_dados_validos.sort(key=lambda p: float(p.glucose))
                    novo_valor = median(float(person.glucose) for person in lista_dados_validos)

                    if pessoa.glucose == '0':
                        lista_dados_validos.clear()
                        pessoa.glucose = str(novo_valor)

                elif dado_checado == 2:
                    for person in cls._lista_de_pessoas:
                        if person.blood_pressure != '0':
                            lista_dados_validos.append(person)

                    lista_dados_validos.sort(key=lambda p: float(p.blood_pressure))
                    novo_valor = median(float(person.blood_pressure) for person in lista_dados_validos)


                    if pessoa.blood_pressure == '0':
                        lista_dados_validos.clear()
                        pessoa.blood_pressure = str(novo_valor)

                elif dado_checado == 3:
                    for person in cls._lista_de_pessoas:
                        if person.skin_thickness != '0':
                            lista_dados_validos.append(person)

                    lista_dados_validos.sort(key=lambda p: float(p.skin_thickness))
                    novo_valor = median(float(person.skin_thickness) for person in lista_dados_validos)

                    if pessoa.skin_thickness == '0':
                        pessoa.skin_thickness = str(novo_valor)
                        lista_dados_validos.clear()

                elif dado_checado == 4:
                    for person in cls._lista_de_pessoas:
                        if person.insulin != '0':
                            lista_dados_validos.append(person)

                    lista_dados_validos.sort(key=lambda p: float(p.insulin))
                    novo_valor = median(float(person.insulin) for person in lista_dados_validos)

                    if pessoa.insulin == '0':
                        lista_dados_validos.clear()
                        pessoa.insulin = str(novo_valor)

                elif dado_checado == 5:
                    for person in cls._lista_de_pessoas:
                        if person.bmi != '0':
                            lista_dados_validos.append(person)

                    lista_dados_validos.sort(key=lambda p: float(p.bmi))
                    novo_valor = median(float(person.bmi) for person in lista_dados_validos)

                    if pessoa.bmi == '0':
                        lista_dados_validos.clear()
                        pessoa.bmi = str(novo_valor)

    @classmethod
    def separar_dados(cls):
        TOTAL_DADOS_TESTE = round(len(cls._lista_de_pessoas) * cls.PORCENTAGEM_DADOS_TESTE)
        TOTAL_DADOS_TREINAMENTO = round(len(cls._lista_de_pessoas)) - TOTAL_DADOS_TESTE

        cls._lista_treinamento = cls._lista_de_pessoas[:TOTAL_DADOS_TREINAMENTO]
        cls._lista_teste = cls._lista_de_pessoas[TOTAL_DADOS_TREINAMENTO:]

    @classmethod
    def checar_dado(cls, pessoa: Person) -> int:

        if not float(pessoa.glucose):
            return 1

        if not float(pessoa.blood_pressure):
            return 2

        if not float(pessoa.skin_thickness):
            return 3

        if not float(pessoa.insulin):
            return 4

        if not float(pessoa.bmi):
            return 5

        return -1