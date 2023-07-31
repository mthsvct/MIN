

class Filme:

    id = 1

    def __init__(self, nome, duracao, genero, ano):
        self.id = Filme.id
        self.nome = nome
        self.duracao = duracao
        self.genero = genero
        self.ano = ano
        self.cabecalho = f"{self.id};{self.nome};{self.duracao};{self.genero};{self.ano}"
        self.dados = [x for x in range(1, self.duracao+1)]
        Filme.id += 1

    def __str__(self): return f"Filme: {self.nome} ({self.ano})"







