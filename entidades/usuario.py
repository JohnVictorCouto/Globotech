from collections import Counter  # Importa Counter para contagem eficiente de elementos em listas

class Usuario:  # Representa um usuário, suas interações e métricas associadas
    def __init__(self, id_usuario):
        # Atributo privado que armazena o ID do usuário
        self.__id_usuario = id_usuario
        # Lista privada que armazenará objetos do tipo Interacao realizados pelo usuário
        self.__interacoes_realizadas = []

    @property
    def id_usuario(self):
        # Retorna o ID do usuário (somente leitura)
        return self.__id_usuario

    @property
    def interacoes_realizadas(self):
        # Retorna a lista de interações feitas pelo usuário (somente leitura)
        return self.__interacoes_realizadas

    def registrar_interacao(self, interacao):
        # Adiciona um objeto Interacao à lista de interações realizadas
        self.__interacoes_realizadas.append(interacao)

    def obter_interacoes_por_tipo(self, tipo_desejado: str) -> list:
        # Retorna uma lista filtrada apenas das interações que correspondem ao tipo_desejado
        return [i for i in self.__interacoes_realizadas if i.tipo_interacao == tipo_desejado]

    def obter_conteudos_unicos_consumidos(self) -> set:
        # Retorna um conjunto (set) contendo os conteúdos únicos consumidos pelo usuário
        conteudos = set()
        for interacao in self.__interacoes_realizadas:
            # Se a interação estiver associada a algum conteúdo, adiciona ao set
            if interacao.conteudo_associado:
                conteudos.add(interacao.conteudo_associado)
        return conteudos

    def calcular_tempo_total_consumo_plataforma(self, plataforma) -> int:
        # Calcula o tempo total (em segundos) que o usuário consumiu em uma dada plataforma
        total_tempo = 0
        for interacao in self.__interacoes_realizadas:
            if interacao.plataforma_interacao == plataforma:
                # Soma o tempo da interação, apenas se for um inteiro positivo
                if isinstance(interacao.watch_duration_seconds, int) and interacao.watch_duration_seconds > 0:
                    total_tempo += interacao.watch_duration_seconds
        return total_tempo

    def plataformas_mais_frequentes(self, top_n=3) -> list:
        # Retorna as top_n plataformas onde o usuário mais interagiu
        plataformas = []
        for interacao in self.__interacoes_realizadas:
            if interacao.plataforma_interacao:
                plataformas.append(interacao.plataforma_interacao)

        # Usa Counter para contar frequências das plataformas na lista
        contagem_plataformas = Counter(plataformas)

        # Retorna as top_n plataformas mais frequentes em forma de lista de tuplas (plataforma, contagem)
        top_plataformas = contagem_plataformas.most_common(top_n)
        return top_plataformas

    def calcular_total_interacoes_engajamento(self):
        # Conta o total de interações do tipo engajamento (like, share, comment)
        total = 0
        for i in self.__interacoes_realizadas:
            if i.tipo_interacao in ["like", "share", "comment"]:
                total += 1
        return total

    def calcular_contagem_por_tipo_interacao(self):
        # Retorna um dicionário com contagem das interações por tipo
        contagem = {}
        for i in self.__interacoes_realizadas:
            tipo = i.tipo_interacao
            if tipo not in contagem:
                contagem[tipo] = 0
            contagem[tipo] += 1
        return contagem

    def calcular_tempo_total_consumo(self):
        # Calcula o tempo total consumido (em segundos) somando todas as interações com duração válida
        total = 0
        for i in self.__interacoes_realizadas:
            if isinstance(i.watch_duration_seconds, int) and i.watch_duration_seconds > 0:
                total += i.watch_duration_seconds
        return total

    def calcular_media_tempo_consumo(self):
        # Calcula a média do tempo consumido nas interações que possuem duração válida
        duracoes = []
        for i in self.__interacoes_realizadas:
            d = i.watch_duration_seconds
            if isinstance(d, int) and d > 0:
                duracoes.append(d)
        if duracoes:
            return sum(duracoes) / len(duracoes)
        else:
            return 0

    def listar_comentarios(self):
        # Retorna uma lista de todos os comentários (texto) feitos pelo usuário
        comentarios = []
        for i in self.__interacoes_realizadas:
            c = i.comment_text
            if c:
                comentarios.append(c)
        return comentarios

    def __str__(self):
        # Representação string simples para impressão
        return f"Usuário ID {self.__id_usuario}"

    def __repr__(self):
        # Representação oficial para debugging, igual a __str__
        return self.__str__()
