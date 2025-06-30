class Fila:
    """
    Implementa uma fila FIFO (First-In, First-Out).
    Operações principais:
    - enfileirar: adicionar elemento no final da fila.
    - desenfileirar: remover e retornar o elemento do início da fila.
    - esta_vazia: verifica se a fila está vazia.
    """

    def __init__(self):
        self._elementos = []

    def enfileirar(self, item):
        """
        Adiciona um item no final da fila.
        Complexidade: O(1)
        """
        self._elementos.append(item)

    def desenfileirar(self):
        """
        Remove e retorna o item do início da fila.
        Se a fila estiver vazia, retorna None.
        Complexidade: O(n), pois lista precisa deslocar elementos.
        """
        if self.esta_vazia():
            return None
        return self._elementos.pop(0)

    def esta_vazia(self):
        """
        Retorna True se a fila estiver vazia, False caso contrário.
        Complexidade: O(1)
        """
        return len(self._elementos) == 0

    def tamanho(self):
        """
        Retorna o tamanho atual da fila.
        Complexidade: O(1)
        """
        return len(self._elementos)
