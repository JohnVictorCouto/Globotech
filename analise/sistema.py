import csv
from collections import defaultdict
from datetime import datetime
from entidades.usuario import Usuario
from entidades.plataforma import Plataforma
from entidades.conteudo import Video, Podcast, Artigo
from entidades.interacao import Interacao

from estruturas_dados.fila import Fila
from estruturas_dados.arvore_binaria_busca import ArvoreBinariaBusca

class SistemaAnaliseEngajamento:

    def __init__(self):
        # Dicionário para plataformas (chave: nome_plataforma)
        self._plataformas_registradas = {}
        # Árvores Binárias de Busca para conteúdos e usuários
        self._arvore_conteudos = ArvoreBinariaBusca()
        self._arvore_usuarios = ArvoreBinariaBusca()
        # Fila para armazenar linhas brutas do CSV
        self._fila_interacoes_brutas = Fila()
        # Contador para gerar IDs para plataformas
        self._proximo_id_plataforma = 1

    # Plataforma continua dicionário, pois poucas plataformas
    def cadastrar_plataforma(self, nome_plataforma):
        if nome_plataforma not in self._plataformas_registradas:
            nova = Plataforma(nome_plataforma, self._proximo_id_plataforma)
            self._plataformas_registradas[nome_plataforma] = nova
            self._proximo_id_plataforma += 1
        return self._plataformas_registradas[nome_plataforma]

    def obter_plataforma(self, nome_plataforma):
        return self._plataformas_registradas.get(nome_plataforma, self.cadastrar_plataforma(nome_plataforma))

    def listar_plataformas(self):
        return list(self._plataformas_registradas.values())

    def carregar_interacoes_csv(self, caminho_arquivo):
        """
        Carrega as linhas do CSV e enfileira na fila _fila_interacoes_brutas.
        Complexidade: O(n), onde n é o número de linhas no CSV.
        """
        try:
            with open(caminho_arquivo, mode='r', encoding='utf-8') as csvfile:
                leitor = csv.DictReader(csvfile, delimiter=';')
                for linha in leitor:
                    self._fila_interacoes_brutas.enfileirar(linha)  # O(1) para enfileirar
        except FileNotFoundError:
            print(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado.")
        except Exception as e:
            print(f"Erro ao carregar CSV: {e}")

    def processar_interacoes_da_fila(self):
        """
        Processa as linhas da fila, criando objetos Plataforma, Conteudo, Usuario e Interacao.
        Complexidade: O(m log n), sendo m o número de interações e n o número de conteúdos/usuários,
        pois inserções e buscas na BST são O(log n) no caso médio.
        """
        while not self._fila_interacoes_brutas.esta_vazia():
            linha = self._fila_interacoes_brutas.desenfileirar()
            try:
                id_usuario = int(linha['id_usuario'])
                id_conteudo = int(linha['id_conteudo'])
                nome_conteudo = linha['nome_conteudo']
                timestamp = linha['timestamp_interacao']
                tipo = linha['tipo_interacao']

                valor_duracao = linha['watch_duration_seconds']
                duracao = int(valor_duracao) if valor_duracao.strip().isdigit() and int(valor_duracao) >= 0 else 0

                comentario = linha['comment_text']
                nome_plataforma = linha['plataforma']
                categoria = linha['categoria'].strip().lower()
                plataforma = self.obter_plataforma(nome_plataforma)

                tipo_conteudo = linha['tipo_conteudo'].strip().lower()

                # Buscar Conteudo na BST
                conteudo = self._arvore_conteudos.buscar(id_conteudo)
                if conteudo is None:
                    # Criar conteúdo conforme tipo (default Video)
                    if tipo_conteudo == "podcast":
                        conteudo = Podcast(id_conteudo, nome_conteudo, 0, categoria)
                    elif tipo_conteudo == "artigo":
                        conteudo = Artigo(id_conteudo, nome_conteudo, 0, categoria)
                    else:
                        conteudo = Video(id_conteudo, nome_conteudo, 0, categoria)

                    conteudo._categoria = categoria
                    self._arvore_conteudos.inserir(conteudo.id_conteudo, conteudo)

                # Buscar Usuario na BST
                usuario = self._arvore_usuarios.buscar(id_usuario)
                if usuario is None:
                    usuario = Usuario(id_usuario)
                    self._arvore_usuarios.inserir(usuario.id_usuario, usuario)

                # Criar interação e associar
                interacao = Interacao(id_usuario, timestamp, tipo, duracao, comentario, conteudo, plataforma)
                conteudo.adicionar_interacao(interacao)
                usuario.registrar_interacao(interacao)

            except Exception as e:
                print(f"Erro ao processar linha: {linha} -> {e}")

    def gerar_relatorio_engajamento_conteudos(self, top_n=None):
        """
        Gera relatório dos conteúdos com maior engajamento.
        Complexidade:
        - Percurso em ordem da BST: O(n), n = número de conteúdos
        - Ordenação Quick Sort: O(n log n) no caso médio
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo registrado para gerar relatório.")
            return

        # Ordenar pelo total de interações
        conteudos_ordenados = self._quick_sort(
            conteudos,
            key=lambda c: c.calcular_total_interacoes_engajamento(),
            reverse=True
        )

        if top_n:
            conteudos_ordenados = conteudos_ordenados[:top_n]

        print("\n-> -> RESULTADOS DE ENGAJAMENTO DE CONTEÚDOS <- <-\n")
        for conteudo in conteudos_ordenados:
            print(f"ID: {conteudo.id_conteudo} - {conteudo.nome_conteudo}")
            print(f"Total de interações: {conteudo.calcular_total_interacoes_engajamento()}")

            contagem_tipos = conteudo.calcular_contagem_por_tipo_interacao()
            if contagem_tipos:
                print("Interações por tipo:")
                for tipo, qtd in contagem_tipos.items():
                    print(f"- {tipo}: {qtd}")

            tempo_total = conteudo.calcular_tempo_total_consumo()
            if tempo_total > 0:
                tempo_medio = conteudo.calcular_media_tempo_consumo()
                print(f"Tempo total assistido: {tempo_total} segundos ou {self.converter_segundos(tempo_total)}")
                print(f"Média de tempo assistido: {tempo_medio:.2f} segundos")

            comentarios = conteudo.listar_comentarios()
            if comentarios:
                print(f"Quantidade de comentários: {len(comentarios)}")
                for idx, c in enumerate(comentarios):
                    print(f"Comentário {idx+1}: {c}")

            print("\n\n")

    def gerar_relatorio_atividade_usuarios(self, top_n=None):
        """
        Gera relatório das atividades dos usuários.
        Complexidade semelhante ao relatório de conteúdos.
        """
        usuarios = [valor for chave, valor in self._arvore_usuarios.percurso_em_ordem()]
        if not usuarios:
            print("Nenhum usuário registrado para gerar relatório.")
            return

        print("\n-> -> RESULTADOS DE ATIVIDADE DE USUÁRIOS <- <-\n")
        for usuario in usuarios:
            print(f"Usuário (ID): {usuario.id_usuario}")
            print(f"Número de Interações: {len(usuario.interacoes_realizadas)}")

            contagem = usuario.calcular_contagem_por_tipo_interacao()
            if contagem:
                print("Contagem por tipo de interação:")
                for tipo, qtd in contagem.items():
                    print(f"             {tipo}: {qtd}")

            total_consumo = usuario.calcular_tempo_total_consumo()
            if total_consumo > 0:
                media_consumo = usuario.calcular_media_tempo_consumo()
                print(f"Tempo total assistido: {total_consumo} segundos ou {self.converter_segundos(total_consumo)}")
                print(f"Média de tempo assistido: {media_consumo:.2f} segundos")

            comentarios = usuario.listar_comentarios()
            if comentarios:
                print(f"Quantidade de comentários: {len(comentarios)}")
                for idx, c in enumerate(comentarios):
                    print(f"Comentário {idx+1}: {c}")

            conteudos_unicos = usuario.obter_conteudos_unicos_consumidos()
            if conteudos_unicos:
                print(f"Conteúdos únicos consumidos: {len(conteudos_unicos)}")

            plataformas_frequentes = usuario.plataformas_mais_frequentes(top_n=5)
            if plataformas_frequentes:
                print("Top 5 Plataformas Mais Frequentes:")
                for plat, cont in plataformas_frequentes:
                    print(f"             {plat.nome_plataforma}: {cont} interação(ões)")

            print("\n\n")

    def gerar_relatorio_top_conteudos_consumidos(self, n=5):
        """
        Gera o ranking dos top N conteúdos pelo tempo total consumido.
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo registrado.")
            return

        conteudos_ordenados = self._quick_sort(
            conteudos,
            key=lambda c: c.calcular_tempo_total_consumo(),
            reverse=True
        )
        top = conteudos_ordenados[:n]

        print("\n-> -> TOP CONTEÚDOS POR TEMPO TOTAL CONSUMIDO <- <-\n")
        for idx, c in enumerate(top):
            tempo_total = c.calcular_tempo_total_consumo()
            print(f"{idx+1}o. {c.nome_conteudo} ({self.converter_segundos(tempo_total)} consumidos)")
    
    def relatorio_comentarios_por_conteudo(self):
        """
        Exibe apenas os comentários agrupados por conteúdo.
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo registrado.")
            return

        print("\n-> -> COMENTÁRIOS POR CONTEÚDO <- <-\n")
        for conteudo in conteudos:
            print(f"Conteúdo: {conteudo.nome_conteudo}")
            comentarios = conteudo.listar_comentarios()
            if comentarios:
                for idx, c in enumerate(comentarios):
                    print(f"  Comentário {idx+1}: {c}")
            else:
                print("  Nenhum comentário registrado.")
            print()

    def relatorio_plataforma_maior_engajamento(self):
        """
        Exibe a(s) plataforma(s) com maior número de interações no sistema.
        """
        # Dicionário para acumular contagem de interações por plataforma
        contagem = {}

        # Percorrer todos os conteúdos e suas interações
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        for conteudo in conteudos:
            for interacao in conteudo._interacoes:
                plataforma = interacao.plataforma_interacao
                if plataforma:
                    nome = plataforma.nome_plataforma
                    contagem[nome] = contagem.get(nome, 0) + 1

        if not contagem:
            print("Nenhuma interação registrada em nenhuma plataforma.")
            return

        # Encontrar maior valor
        max_interacoes = max(contagem.values())
        plataformas_top = [nome for nome, qtd in contagem.items() if qtd == max_interacoes]

        print("\n-> -> PLATAFORMA(S) COM MAIOR ENGAJAMENTO <- <-\n")
        for nome in plataformas_top:
            print(f"Plataforma: {nome} | Total de interações: {max_interacoes}")

    def relatorio_conteudos_mais_comentados(self, top_n=5):
        """
        Gera um relatório com os conteúdos mais comentados.
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo registrado.")
            return

        # Ordena os conteúdos pela quantidade de comentários
        conteudos_ordenados = self._quick_sort(
            conteudos,
            key=lambda c: len(c.listar_comentarios()),
            reverse=True
        )

        top = conteudos_ordenados[:top_n]

        print("\n-> -> CONTEÚDOS MAIS COMENTADOS <- <-\n")
        for idx, c in enumerate(top):
            comentarios = c.listar_comentarios()
            print(f"{idx+1}o. {c.nome_conteudo} - {len(comentarios)} comentário(s)")
            for i, texto in enumerate(comentarios):
                print(f"   Comentário {i+1}: {texto}")
            print()

    def relatorio_tempo_medio_consumo_por_plataforma(self):
        """
        Exibe o tempo médio de consumo por plataforma.
        """
        plataformas = self.listar_plataformas()
        if not plataformas:
            print("Nenhuma plataforma registrada.")
            return

        print("\n-> -> TEMPO MÉDIO DE CONSUMO POR PLATAFORMA <- <-\n")

        for plataforma in plataformas:
            total_tempo = 0
            total_interacoes = 0

            conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
            for conteudo in conteudos:
                for interacao in conteudo._interacoes:
                    if interacao.plataforma_interacao == plataforma:
                        duracao = interacao.watch_duration_seconds
                        if isinstance(duracao, int) and duracao > 0:
                            total_tempo += duracao
                            total_interacoes += 1

            if total_interacoes > 0:
                media = total_tempo / total_interacoes
                print(f"{plataforma.nome_plataforma}: {media:.2f} segundos em média")
            else:
                print(f"{plataforma.nome_plataforma}: Sem dados de consumo.")


    def _ordenar_alfabeticamente_az(self, lista, atributo):
        """
        Ordena uma lista de objetos em ordem alfabética A → Z com base no atributo fornecido.
        """
        return self._quick_sort(lista, key=lambda obj: getattr(obj, atributo).lower(), reverse=False)

    def _ordenar_alfabeticamente_za(self, lista, atributo):
        """
        Ordena uma lista de objetos em ordem alfabética Z → A com base no atributo fornecido.
        """
        return self._quick_sort(lista, key=lambda obj: getattr(obj, atributo).lower(), reverse=True)
    

    def relatorio_conteudos_ordenados_por_nome(self, ordem='AZ'):
        """
        Exibe os conteúdos ordenados alfabeticamente pelo nome.
        
        Parâmetros:
            ordem (str): 'AZ' para ordem crescente (A→Z), 'ZA' para ordem decrescente (Z→A)
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo registrado.")
            return

        if ordem.upper() == 'AZ':
            ordenados = self._ordenar_alfabeticamente_az(conteudos, 'nome_conteudo')
            print("\n-> -> CONTEÚDOS ORDENADOS POR NOME (A → Z) <- <-\n")
        elif ordem.upper() == 'ZA':
            ordenados = self._ordenar_alfabeticamente_za(conteudos, 'nome_conteudo')
            print("\n-> -> CONTEÚDOS ORDENADOS POR NOME (Z → A) <- <-\n")
        else:
            print("Parâmetro 'ordem' inválido. Use 'AZ' ou 'ZA'.")
            return

        for idx, conteudo in enumerate(ordenados):
            print(f"{idx+1} - {conteudo.nome_conteudo}")

    
    def relatorio_total_interacoes_por_tipo_conteudo(self):
        """
        Exibe o total de interações agrupadas por tipo de conteúdo (Video, Podcast, Artigo).
        """
        contagem = {"Video": 0, "Podcast": 0, "Artigo": 0, "Outro": 0}

        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        for conteudo in conteudos:
            tipo = type(conteudo).__name__
            if tipo in contagem:
                contagem[tipo] += len(conteudo._interacoes)
            else:
                contagem["Outro"] += len(conteudo._interacoes)

        print("\n-> -> TOTAL DE INTERAÇÕES POR TIPO DE CONTEÚDO <- <-\n")
        for tipo, qtd in contagem.items():
            print(f"{tipo}: {qtd} interações")

    def relatorio_top_conteudos_mais_visualizados(self, top_n=5):
        """
        Exibe os top N conteúdos com maior número de visualizações iniciadas ('view_start').
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo disponível.")
            return

        # Ordenar pelo número de interações do tipo 'view_start'
        conteudos_ordenados = self._quick_sort(
            conteudos,
            key=lambda c: c.calcular_contagem_por_tipo_interacao().get("view_start", 0),
            reverse=True
        )

        top = conteudos_ordenados[:top_n]

        print("\n-> -> TOP CONTEÚDOS MAIS VISUALIZADOS (view_start) <- <-\n")
        for idx, c in enumerate(top):
            num_views = c.calcular_contagem_por_tipo_interacao().get("view_start", 0)
            print(f"{idx+1}o. {c.nome_conteudo} - {num_views} visualização(ões) iniciadas")

    def relatorio_top_conteudos_mais_curtidos(self, top_n=5):
        """
        Exibe os top N conteúdos com mais curtidas ('like').
        """
        conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]
        if not conteudos:
            print("Nenhum conteúdo disponível.")
            return

        # Ordenar pelos likes
        conteudos_ordenados = self._quick_sort(
            conteudos,
            key=lambda c: c.calcular_contagem_por_tipo_interacao().get("like", 0),
            reverse=True
        )

        top = conteudos_ordenados[:top_n]

        print("\n-> -> TOP CONTEÚDOS MAIS CURTIDOS <- <-\n")
        for idx, c in enumerate(top):
            total_likes = c.calcular_contagem_por_tipo_interacao().get("like", 0)
            print(f"{idx+1}o. {c.nome_conteudo} - {total_likes} curtida(s)")

    def buscar_conteudo_por_nome(self, texto_busca):
        """
        Pesquisa e retorna uma lista de conteúdos cujo nome contenha o texto informado.
        """
        texto_busca = texto_busca.lower()  # Busca case-insensitive
        resultados = []

        # Retorna lista de tuplas (chave, valor)
        todos_conteudos = self._arvore_conteudos.percurso_em_ordem()

        # Itera desempacotando a tupla para acessar o objeto Conteudo (valor)
        for _, conteudo in todos_conteudos:
            if texto_busca in conteudo.nome_conteudo.lower():
                resultados.append(conteudo)

        return resultados

    def buscar_conteudos_por_plataforma(self, nome_plataforma):
        """
        Retorna uma lista de conteúdos que tiveram interações associadas à plataforma especificada.
        """
        nome_plataforma = nome_plataforma.strip().lower()
        conteudos_encontrados = set()

        todos_conteudos = [valor for chave, valor in self._arvore_conteudos.percurso_em_ordem()]

        for conteudo in todos_conteudos:
            for interacao in conteudo._interacoes:
                if interacao.plataforma_interacao and interacao.plataforma_interacao.nome_plataforma.lower() == nome_plataforma:
                    conteudos_encontrados.add(conteudo)
                    break 

        return list(conteudos_encontrados)

    def relatorio_distribuicao_interacoes_por_plataforma(self):
        """
        Exibe a distribuição de tipos de interações por plataforma.
        """
        distribuicao = defaultdict(lambda: defaultdict(int))

        # Percorre todos os conteúdos na BST
        conteudos = [valor for _, valor in self._arvore_conteudos.percurso_em_ordem()]
        for conteudo in conteudos:
            for interacao in conteudo._interacoes:
                plataforma = interacao.plataforma_interacao.nome_plataforma if interacao.plataforma_interacao else "Desconhecida"
                tipo = interacao.tipo_interacao
                distribuicao[plataforma][tipo] += 1

        print("\nDistribuição de interações por plataforma:\n")
        for plataforma, tipos in distribuicao.items():
            print(f"Plataforma: {plataforma}")
            for tipo, quantidade in tipos.items():
                print(f"- {tipo.capitalize()}: {quantidade}")
            print()

    def recomendar_conteudos_por_categoria(self, categoria, top_n=5, peso_interacoes=0.6, peso_tempo=0.4):
        """
        Recomenda conteúdos da categoria informada, ordenando por uma métrica combinada
        de engajamento (número de interações) e tempo total assistido.

        Parâmetros:
            categoria (str): categoria desejada para recomendação
            top_n (int): quantidade máxima de conteúdos recomendados
            peso_interacoes (float): peso para o total de interações (0 a 1)
            peso_tempo (float): peso para o tempo total consumido (0 a 1)
        Retorna:
            lista de conteúdos recomendados (objetos Conteudo)
        """

        # Obter todos os conteúdos da categoria solicitada
        conteudos_da_categoria = [
            conteudo for _, conteudo in self._arvore_conteudos.percurso_em_ordem()
            if conteudo.categoria and conteudo.categoria.lower() == categoria.lower()
        ]

        if not conteudos_da_categoria:
            print(f"Nenhum conteúdo encontrado para a categoria '{categoria}'.")
            return []

        # Calcular métrica combinada para cada conteúdo
        lista_pontuacoes = []
        for conteudo in conteudos_da_categoria:
            total_interacoes = conteudo.calcular_total_interacoes_engajamento()
            tempo_total = conteudo.calcular_tempo_total_consumo()

            # Caso não haja máximo > 0, usar 1 para evitar divisão por zero.

            max_interacoes = max(c.calcular_total_interacoes_engajamento() for c in conteudos_da_categoria) or 1
            max_tempo = max(c.calcular_tempo_total_consumo() for c in conteudos_da_categoria) or 1

            pontuacao = (
                peso_interacoes * (total_interacoes / max_interacoes) +
                peso_tempo * (tempo_total / max_tempo)
            )
            lista_pontuacoes.append((conteudo, pontuacao))

        # Ordenar pelos scores descendentes
        lista_pontuacoes.sort(key=lambda x: x[1], reverse=True)

        # Pegar os top_n conteúdos recomendados
        recomendados = [item[0] for item in lista_pontuacoes[:top_n]]

        return recomendados


    def converter_segundos(self, total_segundos):
        """
        Converte segundos em formato HH:MM:SS.
        """
        if not isinstance(total_segundos, (int, float)) or total_segundos < 0:
            return "0:00:00"
        horas = int(total_segundos // 3600)
        minutos = int((total_segundos % 3600) // 60)
        segundos = int(total_segundos % 60)
        return f"{horas}:{minutos:02}:{segundos:02}"

    # --- Algoritmos de Ordenação ---

    def _quick_sort(self, array, key=lambda x: x, low=0, high=None, reverse=False):
        """
        Quick Sort para ordenar listas.
        Tempo médio: O(n log n), pior caso: O(n²).
        """
        if high is None:
            high = len(array) - 1

        def partition(arr, low, high):
            pivot = key(arr[high])
            i = low - 1
            for j in range(low, high):
                if (key(arr[j]) > pivot if reverse else key(arr[j]) < pivot):
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
            arr[i+1], arr[high] = arr[high], arr[i+1]
            return i + 1

        if low < high:
            pi = partition(array, low, high)
            self._quick_sort(array, key, low, pi - 1, reverse)
            self._quick_sort(array, key, pi + 1, high, reverse)
        return array

    def _insertion_sort(self, array, key=lambda x: x, reverse=False):
        """
        Insertion Sort para ordenar listas pequenas.
        Tempo: O(n²) no geral, eficiente para listas pequenas.
        """
        for i in range(1, len(array)):
            current = array[i]
            j = i - 1
            while j >= 0 and ((key(array[j]) < key(current)) if reverse else (key(array[j]) > key(current))):
                array[j + 1] = array[j]
                j -= 1
            array[j + 1] = current
        return array
