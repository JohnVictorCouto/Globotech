from datetime import datetime
from entidades.plataforma import Plataforma
from entidades.conteudo import Conteudo

class Interacao:
    TIPOS_INTERACAO_VALIDOS = {"view_start", "like", "share", "comment", "vote_bbb"}
    __proximo_id = 1  # Contador para gerar IDs únicos para interações

    def __init__(self, id_usuario, timestamp, tipo_interacao, watch_duration_seconds=0, comment_text="", conteudo_associado=None, plataforma_interacao=None):
        self.__interacao_id = Interacao.__proximo_id
        Interacao.__proximo_id += 1

        self.__id_usuario = int(id_usuario)

        # Tenta converter timestamp para datetime; se inválido, define como datetime.min
        try:
            self.__timestamp_interacao = datetime.fromisoformat(timestamp)
        except ValueError:
            self.__timestamp_interacao = datetime.min
        
        # Valida o tipo de interação, padrão para "view_start" se inválido
        self.__tipo_interacao = tipo_interacao if tipo_interacao in self.TIPOS_INTERACAO_VALIDOS else "view_start"

        # Valida duração do watch, nunca negativa
        try:
            self.__watch_duration_seconds = int(watch_duration_seconds)
            if self.__watch_duration_seconds < 0:
                self.__watch_duration_seconds = 0
        except (ValueError, TypeError):
            self.__watch_duration_seconds = 0

        self.__comment_text = comment_text.strip() if comment_text else ""
        self.__conteudo_associado = conteudo_associado
        self.__plataforma_interacao = plataforma_interacao

    @property
    def interacao_id(self):
        return self.__interacao_id

    @property
    def conteudo_associado(self):
        return self.__conteudo_associado

    @property
    def plataforma_interacao(self):
        return self.__plataforma_interacao

    @property
    def id_usuario(self):
        return self.__id_usuario

    @property
    def timestamp_interacao(self):
        return self.__timestamp_interacao

    @property
    def tipo_interacao(self):
        return self.__tipo_interacao

    @property
    def watch_duration_seconds(self):
        return self.__watch_duration_seconds

    @property
    def comment_text(self):
        return self.__comment_text

    def __lt__(self, other):
        if not isinstance(other, Interacao):
            return NotImplemented
        # Ordena pela data da interação (timestamp)
        return self.__timestamp_interacao < other.timestamp_interacao

    def __str__(self):
        return f"Interação {self.__interacao_id}: {self.__tipo_interacao} por usuário {self.__id_usuario} em {self.conteudo_associado.nome_conteudo}"

    def __repr__(self):
        return (f"Interacao(id={self.__interacao_id}, usuario={self.__id_usuario}, tipo='{self.__tipo_interacao}', "
                f"duracao={self.__watch_duration_seconds}, comentario='{self.__comment_text}')")
