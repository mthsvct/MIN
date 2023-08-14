class CliFilme:

    def __init__(
        self,
        id:int=None,
        nome:str=None,
        ano:int=None,
        genero:str=None,
        duracao:int=None
    ) -> None:
        self.id = id
        self.nome = nome
        self.ano = ano
        self.genero = genero
        self.duracao = duracao
        self.cabecalho = f"{self.id};{self.nome};{self.ano};{self.genero};{self.duracao};"
        self.dados:list = []

    def __str__(self) -> str:
        return f"{self.id} - {self.nome} ({self.ano}) - {self.duracao} min"