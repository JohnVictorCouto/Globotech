class Plataforma:
    def __init__(self, nome_plataforma, id_plataforma=None):
        # Cria nova instância de plataforma
        if not nome_plataforma or not nome_plataforma.strip():
            raise ValueError("Nome da plataforma não pode ser vazio.")
        self.__nome_plataforma = nome_plataforma.strip()
        self.__id_plataforma = id_plataforma

    @property
    def nome_plataforma(self):
        return self.__nome_plataforma

    @nome_plataforma.setter
    def nome_plataforma(self, valor):
        if not valor or not valor.strip():
            raise ValueError("Nome da plataforma não pode ser vazio.")
        self.__nome_plataforma = valor.strip()

    @property
    def id_plataforma(self):
        return self.__id_plataforma

    @id_plataforma.setter
    def id_plataforma(self, valor):
        self.__id_plataforma = valor

    def __str__(self):
        return self.__nome_plataforma

    def __repr__(self):
        return f"Plataforma(nome='{self.__nome_plataforma}')"

    def __eq__(self, other):
        if isinstance(other, Plataforma):
            return self.__nome_plataforma == other.__nome_plataforma
        return False

    def __hash__(self):
        return hash(self.__nome_plataforma)

    def __lt__(self, other):
        if not isinstance(other, Plataforma):
            return NotImplemented
        # Ordena pela id_plataforma se ambos tiverem, senão pelo nome
        if self.__id_plataforma is not None and other.id_plataforma is not None:
            return self.__id_plataforma < other.id_plataforma
        return self.__nome_plataforma < other.nome_plataforma
