##  Funcionalidades e Complexidade Algorítmica

### Carregamento e Processamento

| Método | Descrição | Complexidade |
|--------|-----------|--------------|
| `carregar_interacoes_csv(caminho_arquivo)` | Lê o CSV e armazena cada linha em uma fila | **O(n)** |
| `processar_interacoes_da_fila()` | Cria objetos e insere nas BSTs | **O(m log n)** |

---

### Relatórios de Conteúdo

| Método | Função | Complexidade |
|--------|--------|--------------|
| `gerar_relatorio_engajamento_conteudos(top_n)` | Relatório geral de engajamento | **O(n log n)** |
| `relatorio_top_conteudos_consumidos(n)` | Ranking por tempo assistido | **O(n log n)** |
| `relatorio_conteudos_mais_comentados(top_n)` | Ranking por comentários | **O(n log n)** |
| `relatorio_top_conteudos_mais_visualizados(top_n)` | Ranking por views | **O(n log n)** |
| `relatorio_top_conteudos_mais_curtidos(top_n)` | Ranking por curtidas | **O(n log n)** |
| `relatorio_conteudos_ordenados_por_nome(ordem)` | Ordenação alfabética | **O(n log n)** |
| `relatorio_total_interacoes_por_tipo_conteudo()` | Agrupamento por tipo | **O(n)** |
| `relatorio_comentarios_por_conteudo()` | Comentários por conteúdo | **O(n + c)** |

---

###  Relatórios de Usuários

| Método | Função | Complexidade |
|--------|--------|--------------|
| `gerar_relatorio_atividade_usuarios(top_n)` | Atividades por usuário | **O(u)** |
| `usuario.calcular_tempo_total_consumo()` | Soma tempo de consumo | **O(k)** |

---

###  Relatórios de Plataforma

| Método | Função | Complexidade |
|--------|--------|--------------|
| `relatorio_plataforma_maior_engajamento()` | Mais interações | **O(n * i)** |
| `relatorio_tempo_medio_consumo_por_plataforma()` | Tempo médio assistido | **O(n * i)** |
| `relatorio_distribuicao_interacoes_por_plataforma()` | Tipos por plataforma | **O(n * i)** |

---

###  Buscas e Filtros

| Método | Função | Complexidade |
|--------|--------|--------------|
| `buscar_conteudo_por_nome(texto)` | Busca por nome | **O(n)** |
| `buscar_conteudos_por_plataforma(nome)` | Conteúdos por plataforma | **O(n * i)** |

---

###  Recomendação

| Método | Função | Complexidade |
|--------|--------|--------------|
| `recomendar_conteudos_por_categoria()` | Ranking combinado | **O(n log n)** |

---

##  Estruturas de Dados e Ordenações

| Estrutura / Algoritmo | Utilização | Complexidade |
|-----------------------|------------|--------------|
| `Fila` | Interações brutas | O(1) |
| `BST` | Conteúdos/usuários | O(log n) médio |
| `Quick Sort` | Ordenação geral | O(n log n) médio |
| `Insertion Sort` | Listas pequenas | O(n²) |

---

## ⏱️ Conversão de Tempo

- `converter_segundos(segundos)` → **O(1)**

---

## Notação Usada

- `n` = quantidade de conteúdos  
- `m` = quantidade de interações (linhas no CSV)  
- `u` = número de usuários  
- `i` = número médio de interações por conteúdo  
- `k` = número de interações por usuário  
- `c` = número de comentários por conteúdo  


## 📂 Estrutura do CSV

```
id_usuario;id_conteudo;nome_conteudo;timestamp_interacao;tipo_interacao;watch_duration_seconds;comment_text;plataforma;categoria;tipo_conteudo
```

---
