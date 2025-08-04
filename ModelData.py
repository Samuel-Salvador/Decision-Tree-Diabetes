class ModelData:

    @classmethod
    def get_var_from_values_and_atr(cls, atr, valor) -> str:

        value = float(valor)

        if atr == '_glucose':
            if value < 65:
                return 'baixo'
            elif 54 <= value < 100:
                return 'normal'
            elif 100 <= value < 125:
                return 'alto'
            elif value >= 125:
                return 'altissimo'

        elif atr == '_pregnancies':
            if value < 4 :
                return 'normal'
            elif value >= 4:
                return 'elevado'

        elif atr == '_blood_pressure':
            if value < 50:
                return 'baixo'
            elif 50 <= value < 80:
                return 'normal'
            elif value >= 80:
                return 'alto'

        elif atr == '_skin_thickness':
            if value < 20:
                return 'normal'
            elif value >= 20:
                return 'elevado'

        elif atr == '_insulin':
            if value < 140 :
                return 'normal'
            elif 140 <= value < 200:
                return 'elevado'
            elif value >= 200:
                return 'altissimo'

        elif atr == '_bmi':
            if value < 25:
                return 'normal'
            elif 25 <= value < 30:
                return 'sobrepeso'
            elif value >= 30:
                return 'obesidade'

        elif atr == '_diabetes_pedigree_function':
            if value < 0.5:
                return 'baixo'
            elif 0.5 <= value < 1.0:
                return 'moderado'
            elif value >= 1.0:
                return 'alto'

        elif atr == '_age':
            if value < 35:
                return 'jovem'
            elif 35 <= value < 55:
                return 'adulto'
            elif value >= 55:
                return 'idoso'

        raise AttributeError('atributo não encontrado')

    def __init__(self):
        self._dados = {
            '_pregnancies': {
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'elevado': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_glucose': {
                'baixo': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'alto': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'altissimo': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_blood_pressure': {
                'baixo': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'alto': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_skin_thickness': {
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'elevado': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_insulin': {
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'elevado': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'altissimo': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_bmi': {
                'normal': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'sobrepeso': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'obesidade': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_diabetes_pedigree_function': {
                'baixo': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'moderado': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'alto': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            },

            '_age': {
                'jovem': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'adulto': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'idoso': {'lista_pessoas': [], 'qnt_diabeticos': 0},
                'qnt_diabeticos_atr': 0,
                'qnt_pessoas': 0
            }
        }

    @property
    def dados(self):
        return self._dados

    @dados.setter
    def dados(self, value):
        self._dados = value

