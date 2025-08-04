class Person:

    def __init__(self, *args):
        for conjunto_de_dados in args:
            self._pregnancies = conjunto_de_dados[0]
            self._glucose = conjunto_de_dados[1]
            self._blood_pressure = conjunto_de_dados[2]
            self._skin_thickness = conjunto_de_dados[3]
            self._insulin = conjunto_de_dados[4]
            self._bmi = conjunto_de_dados[5]
            self._diabetes_pedigree_function = conjunto_de_dados[6]
            self._age = conjunto_de_dados[7]
            self._outcome = conjunto_de_dados[8]

    @property
    def pregnancies(self):
        return self._pregnancies

    @property
    def glucose(self):
        return self._glucose

    @glucose.setter
    def glucose(self, novo_valor):
        self._glucose = novo_valor

    @property
    def blood_pressure(self):
        return self._blood_pressure

    @blood_pressure.setter
    def blood_pressure(self, novo_valor):
        self._blood_pressure = novo_valor

    @property
    def skin_thickness(self):
        return self._skin_thickness

    @skin_thickness.setter
    def skin_thickness(self, novo_valor):
        self._skin_thickness = novo_valor

    @property
    def insulin(self):
        return self._insulin

    @insulin.setter
    def insulin(self, novo_valor):
        self._insulin = novo_valor

    @property
    def bmi(self):
        return self._bmi

    @bmi.setter
    def bmi(self, novo_valor):
        self._bmi = novo_valor

    @property
    def diabetes_pedigree_function(self):
        return self._diabetes_pedigree_function

    @property
    def age(self):
        return self._age

    @property
    def outcome(self):
        return self._outcome

    def print_todos_dados(self):
        print(f'Gravidezes: {self.pregnancies}\n'
              f'Glicose: {self.glucose}\n'
              f'Pressão-Sanguínea: {self.blood_pressure}\n'
              f'Grossura da Pele: {self.skin_thickness}\n'
              f'Insulina: {self.insulin}\n'
              f'IMC: {self.bmi}\n'
              f'Predisposição Genética: {self._diabetes_pedigree_function}\n'
              f'Idade: {self.age}\n'
              f'Resultado: {self.outcome}\n')
