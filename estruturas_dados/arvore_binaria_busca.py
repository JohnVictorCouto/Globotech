class NoArvore:
    """
    Nó da Árvore Binária de Busca.
    Cada nó armazena uma chave (id), o valor (objeto) e referências para os filhos esquerdo e direito.
    """

    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.esquerdo = None
        self.direito = None

class ArvoreBinariaBusca:
    """
    Implementação de uma Árvore Binária de Busca (BST).
    Chave: inteiro (ex: id do conteúdo ou usuário)
    Valor: objeto associado (ex: Conteudo ou Usuario)

    Operações:
    - inserir: insere um novo nó.
    - buscar: retorna o valor dado a chave.
    - remover: remove um nó pela chave.
    - percurso_em_ordem: retorna lista dos valores em ordem crescente das chaves.

    Complexidades médias:
    - Inserção, busca e remoção: O(log n) em árvores balanceadas,
      mas pode degradar para O(n) em piores casos (árvore degenerada).
    """

    def __init__(self):
        self.raiz = None

    def inserir(self, chave, valor):
        """
        Insere um novo nó na árvore.
        Se a chave já existir, substitui o valor.
        """
        self.raiz = self._inserir_rec(self.raiz, chave, valor)

    def _inserir_rec(self, no_atual, chave, valor):
        if no_atual is None:
            return NoArvore(chave, valor)
        if chave < no_atual.chave:
            no_atual.esquerdo = self._inserir_rec(no_atual.esquerdo, chave, valor)
        elif chave > no_atual.chave:
            no_atual.direito = self._inserir_rec(no_atual.direito, chave, valor)
        else:
            # Chave já existe, atualiza valor
            no_atual.valor = valor
        return no_atual

    def buscar(self, chave):
        """
        Busca o valor associado à chave.
        Retorna None se não encontrar.
        """
        return self._buscar_rec(self.raiz, chave)

    def _buscar_rec(self, no_atual, chave):
        if no_atual is None:
            return None
        if chave == no_atual.chave:
            return no_atual.valor
        elif chave < no_atual.chave:
            return self._buscar_rec(no_atual.esquerdo, chave)
        else:
            return self._buscar_rec(no_atual.direito, chave)

    def remover(self, chave):
        """
        Remove o nó com a chave especificada.
        """
        self.raiz = self._remover_rec(self.raiz, chave)

    def _remover_rec(self, no_atual, chave):
        if no_atual is None:
            return None

        if chave < no_atual.chave:
            no_atual.esquerdo = self._remover_rec(no_atual.esquerdo, chave)
        elif chave > no_atual.chave:
            no_atual.direito = self._remover_rec(no_atual.direito, chave)
        else:
            # Nó encontrado
            # Caso 1: Nó sem filhos
            if no_atual.esquerdo is None and no_atual.direito is None:
                return None
            # Caso 2: Nó com um filho
            if no_atual.esquerdo is None:
                return no_atual.direito
            if no_atual.direito is None:
                return no_atual.esquerdo
            # Caso 3: Nó com dois filhos
            # Encontra o menor nó da subárvore direita (sucessor)
            sucessor = self._minimo(no_atual.direito)
            no_atual.chave = sucessor.chave
            no_atual.valor = sucessor.valor
            # Remove o sucessor da subárvore direita
            no_atual.direito = self._remover_rec(no_atual.direito, sucessor.chave)
        return no_atual

    def _minimo(self, no):
        """
        Retorna o nó com a menor chave na subárvore.
        """
        atual = no
        while atual.esquerdo is not None:
            atual = atual.esquerdo
        return atual

    def percurso_em_ordem(self):
        resultado = []
        self._em_ordem_rec(self.raiz, resultado)
        return resultado  # Lista de (chave, valor)

    def _em_ordem_rec(self, no, resultado):
        if no is not None:
            self._em_ordem_rec(no.esquerdo, resultado)
            resultado.append((no.chave, no.valor))  # retorna tuplas
            self._em_ordem_rec(no.direito, resultado)