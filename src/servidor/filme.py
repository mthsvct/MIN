

class Filme:

    total = 0

    def __init__(self, nome:str, duracao:int, ano:int, genero:str) -> None:
        self.id = Filme.total
        Filme.total += 1
        self.nome = nome
        self.duracao = duracao
        self.ano = ano
        self.genero = genero
    
