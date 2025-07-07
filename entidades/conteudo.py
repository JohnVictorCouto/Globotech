from entidades.plataforma import Plataforma

class Conteudo:
    def __init__(self, id_conteudo, nome_conteudo,categoria):
        self._id_conteudo = id_conteudo
        self._nome_conteudo = nome_conteudo
        self._interacoes = []
        self._categoria = categoria

    @property
    def id_conteudo(self):
        return self._id_conteudo

    @property
    def nome_conteudo(self):
        return self._nome_conteudo

    @property
    def categoria(self):
        return self._categoria

    def adicionar_interacao(self, interacao):
        self._interacoes.append(interacao)

    def calcular_total_interacoes_engajamento(self):
        total = 0
        for i in self._interacoes:
            if i.tipo_interacao in ["like", "share", "comment","view_start"]:
                total += 1
        return total

    def calcular_contagem_por_tipo_interacao(self):
        contagem = {}
        for i in self._interacoes:
            tipo = i.tipo_interacao
            contagem[tipo] = contagem.get(tipo, 0) + 1
        return contagem

    def calcular_tempo_total_consumo(self):
        total = 0
        for i in self._interacoes:
            if isinstance(i.watch_duration_seconds, int) and i.watch_duration_seconds > 0:
                total += i.watch_duration_seconds
        return total

    def calcular_media_tempo_consumo(self):
        duracoes = [i.watch_duration_seconds for i in self._interacoes if isinstance(i.watch_duration_seconds, int) and i.watch_duration_seconds > 0]
        if duracoes:
            return sum(duracoes) / len(duracoes)
        return 0

    def listar_comentarios(self):
        comentarios = []
        for i in self._interacoes:
            c = i.comment_text
            if c is not None and c.strip() != "":
                comentarios.append(c)
        return comentarios

    def __str__(self):
        return f"Conteúdo ID {self._id_conteudo}: {self._nome_conteudo}"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        if isinstance(other, Conteudo):
            return self._id_conteudo < other._id_conteudo
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Conteudo):
            return self._id_conteudo == other._id_conteudo
        return NotImplemented

    def __hash__(self):
        return hash(self._id_conteudo)


class Video(Conteudo):
    def __init__(self, id_conteudo, nome_conteudo, duracao_total_video_seg, categoria=None):
        super().__init__(id_conteudo, nome_conteudo, categoria)
        self.__duracao_total_video_seg = duracao_total_video_seg

    @property
    def duracao_total_video_seg(self):
        return self.__duracao_total_video_seg

    def calcular_percentual_medio_assistido(self):
        if self.__duracao_total_video_seg == 0:
            return 0
        media = self.calcular_media_tempo_consumo()
        return (media / self.__duracao_total_video_seg) * 100


class Podcast(Conteudo):
    def __init__(self, id_conteudo, nome_conteudo, duracao_total_episodio_seg=0, categoria=None):
        super().__init__(id_conteudo, nome_conteudo, categoria)
        self.__duracao_total_episodio_seg = duracao_total_episodio_seg

    @property
    def duracao_total_episodio_seg(self):
        return self.__duracao_total_episodio_seg


class Artigo(Conteudo):
    def __init__(self, id_conteudo, nome_conteudo, tempo_leitura_estimado_seg=0, categoria=None):
        super().__init__(id_conteudo, nome_conteudo, categoria)
        self.__tempo_leitura_estimado_seg = tempo_leitura_estimado_seg

    @property
    def tempo_leitura_estimado_seg(self):
        return self.__tempo_leitura_estimado_seg
