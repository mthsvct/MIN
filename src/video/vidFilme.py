


class VidFilme:

    def __init__(self, id:int, nome:str, duracao:int, genero:str, ano:int, dados=None):
        self.id = id
        self.nome = nome
        self.duracao = duracao
        self.genero = genero
        self.ano = ano
        self.cabecalho = f"{self.id};{self.nome};{self.duracao};{self.genero};{self.ano}"
        self.dados = dados

    def __str__(self): return f"{self.nome} ({self.ano})"

