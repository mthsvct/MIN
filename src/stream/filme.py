


class Filme:

    id = 1

    def __init__(
        self,
        nome:str=None,
        ano:int=None,
        genero:str=None,
        duracao:int=None
    ) -> None:
        self.id = Filme.id
        self.nome = nome
        self.ano = ano
        self.genero = genero
        self.duracao = duracao
        self.cabecalho = f"{self.id};{self.nome};{self.ano};{self.genero};{self.duracao}"
        self.dados = [x for x in range(1, self.duracao+1)]
        Filme.id += 1