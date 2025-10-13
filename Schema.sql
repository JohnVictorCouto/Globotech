-- Cria o banco de dados caso ele ainda não exista
CREATE DATABASE IF NOT EXISTS globo_tech;

-- Usa o banco de dados 'globo_tech'
USE globo_tech;

-- Cria a tabela 'Plataforma' caso ainda não exista
CREATE TABLE IF NOT EXISTS Plataforma (
    -- Define o nome da plataforma como chave primária e tipo texto (até 100 caracteres)
    id_plataforma INT AUTO_INCREMENT PRIMARY KEY,
    nome_plataforma VARCHAR(100) NOT NULL UNIQUE
);

-- Cria a tabela 'Usuario' caso ainda não exista
CREATE TABLE IF NOT EXISTS Usuario (
    -- Define o id do usuário como chave primária e tipo inteiro
    id_usuario INT PRIMARY KEY
);

-- Cria a tabela 'Conteudo' caso ainda não exista
CREATE TABLE IF NOT EXISTS Conteudo (
    -- Identificador único do conteúdo, chave primária
    id_conteudo INT PRIMARY KEY,
    -- Nome do conteúdo, até 255 caracteres
    nome_conteudo VARCHAR(255) NOT NULL,
    -- Tipo do conteúdo (ex: vídeo, podcast), até 50 caracteres
    tipo_conteudo VARCHAR(50) NOT NULL
);

-- Cria a tabela 'Categoria' caso ainda não exista
CREATE TABLE IF NOT EXISTS Categoria (
    -- Identificador da categoria, chave primária com incremento automático
    id_categoria INT AUTO_INCREMENT PRIMARY KEY,
    -- Nome da categoria, único no banco (ex: Jornalismo, Entretenimento)
    nome_categoria VARCHAR(100) NOT NULL UNIQUE
);

-- Cria a tabela de associação entre conteúdo e categorias (relação N para N)
CREATE TABLE IF NOT EXISTS ConteudoCategoria (
    -- Chave estrangeira para o conteúdo
    id_conteudo INT,
    -- Chave estrangeira para a categoria
    id_categoria INT,
    -- Define a combinação dos dois campos como chave primária (evita duplicatas)
    PRIMARY KEY (id_conteudo, id_categoria),
    -- Relaciona id_conteudo com a tabela Conteudo
    FOREIGN KEY (id_conteudo) REFERENCES Conteudo(id_conteudo),
    -- Relaciona id_categoria com a tabela Categoria
    FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria)
);

-- Cria a tabela que registra as interações dos usuários com os conteúdos
CREATE TABLE IF NOT EXISTS Interacao (
    -- Identificador único da interação, chave primária com incremento automático
    id_interacao INT AUTO_INCREMENT PRIMARY KEY,
    -- Chave estrangeira para o conteúdo associado à interação
    id_conteudo INT,
    -- Chave estrangeira para o usuário que interagiu
    id_usuario INT,
    -- Chave estrangeira para a plataforma usada
    id_plataforma INT,
    -- Data e hora da interação
    timestamp_interacao DATETIME,
    -- Tipo de interação (ex: view_start, like, comment)
    tipo_interacao VARCHAR(50),
    -- Duração da visualização (em segundos), se aplicável
    watch_duration_seconds INT,
    -- Texto do comentário, se houver
    comment_text TEXT,
    -- Relaciona id_conteudo com a tabela Conteudo
    FOREIGN KEY (id_conteudo) REFERENCES Conteudo(id_conteudo),
    -- Relaciona id_usuario com a tabela Usuario
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    -- Relaciona id_plataforma com a tabela Plataforma
    FOREIGN KEY (id_plataforma) REFERENCES Plataforma(id_plataforma)
);

-- Consultas
-- Relatório geral de engajamento (Top N)
SELECT
  c.id_conteudo,
  c.nome_conteudo,
  COUNT(i.id_interacao) AS total_interacoes,
  SUM(i.watch_duration_seconds) AS tempo_total,
  SUM(i.tipo_interacao = 'like') AS curtidas,
  SUM(i.tipo_interacao = 'comment') AS comentarios,
  SUM(i.tipo_interacao = 'view_start') AS visualizacoes
FROM Conteudo c
JOIN Interacao i ON c.id_conteudo = i.id_conteudo
GROUP BY c.id_conteudo
ORDER BY total_interacoes DESC;

-- Gerar Relatório de Atividade de Usuários
SELECT id_usuario, COUNT(*) AS total_interacoes
FROM Interacao
GROUP BY id_usuario
ORDER BY total_interacoes DESC;

-- Top 5 Conteúdos por Tempo Total Consumido
SELECT c.nome_conteudo, SUM(i.watch_duration_seconds) AS tempo_total
FROM Conteudo c
JOIN Interacao i ON c.id_conteudo = i.id_conteudo
GROUP BY c.id_conteudo
ORDER BY tempo_total DESC
LIMIT 5;

-- Top 5 Conteúdos Mais Curtidos
SELECT c.nome_conteudo, COUNT(*) AS total_curtidas
FROM Conteudo c
JOIN Interacao i ON c.id_conteudo = i.id_conteudo
WHERE i.tipo_interacao = 'like'
GROUP BY c.id_conteudo
ORDER BY total_curtidas DESC
LIMIT 5;

-- Top 5 Conteúdos Mais Visualizados
SELECT c.nome_conteudo, COUNT(*) AS total_views
FROM Conteudo c
JOIN Interacao i ON c.id_conteudo = i.id_conteudo
WHERE i.tipo_interacao = 'view_start'
GROUP BY c.id_conteudo
ORDER BY total_views DESC
LIMIT 5;

-- Plataformas com Maior Engajamento
SELECT p.id_plataforma, p.nome_plataforma, COUNT(*) AS total_interacoes
FROM Interacao i
JOIN Plataforma p ON i.id_plataforma = p.id_plataforma
GROUP BY p.id_plataforma, p.nome_plataforma
ORDER BY total_interacoes DESC;

-- Total de Interações por Tipo de Conteúdo
SELECT c.tipo_conteudo, COUNT(*) AS total_interacoes
FROM Interacao i
JOIN Conteudo c ON i.id_conteudo = c.id_conteudo
GROUP BY c.tipo_conteudo
ORDER BY total_interacoes DESC;

-- Tempo Médio de Consumo por Plataforma
SELECT p.id_plataforma, p.nome_plataforma, AVG(i.watch_duration_seconds) AS tempo_medio
FROM Interacao i
JOIN Plataforma p ON i.id_plataforma = p.id_plataforma
WHERE i.watch_duration_seconds IS NOT NULL
GROUP BY p.id_plataforma, p.nome_plataforma
ORDER BY tempo_medio DESC;

-- Comentários por Conteúdo
SELECT c.nome_conteudo, i.comment_text
FROM Interacao i
JOIN Conteudo c ON i.id_conteudo = c.id_conteudo
WHERE i.comment_text IS NOT NULL
ORDER BY c.nome_conteudo;

-- Ordenar Conteúdos de A - Z
SELECT * FROM Conteudo
ORDER BY nome_conteudo ASC;

-- Ordenar Conteúdos de Z - A
SELECT * FROM Conteudo
ORDER BY nome_conteudo DESC;

-- Pesquisar Conteudo
SELECT * FROM Conteudo
WHERE nome_conteudo LIKE '%Brasil%'; -- Pode mudar

-- Pesquisar Plataforma e Listar Conteúdos Associados
SELECT DISTINCT c.nome_conteudo
FROM Interacao i
JOIN Conteudo c ON i.id_conteudo = c.id_conteudo
JOIN Plataforma p ON i.id_plataforma = p.id_plataforma
WHERE p.nome_plataforma = 'Globoplay'; -- Pode mudar

-- Recomendar Conteudo por Categoria em um Ranking
/*
Recomenda conteúdos da categoria informada + conteúdos de outras categorias,
separados em duas listas, ordenados por uma métrica combinada de engajamento e tempo total assistido.

peso_interacoes (float): peso para o total de interações (0 a 1).
peso_tempo (float): peso para o tempo total consumido (0 a 1). 
*/
-- Define a categoria desejada
SET @categoria := 'Música'; -- Pode mudar
-- Define a pesos
SET @peso_interacoes := 0.6;
SET @peso_tempo := 0.4;

-- Parte 1: Top 5 conteúdos da categoria desejada
(
    SELECT *
    FROM (
        SELECT
            c.id_conteudo,
            c.nome_conteudo,
            GROUP_CONCAT(DISTINCT cat.nome_categoria) AS categorias,
            COUNT(i.id_interacao) AS total_interacoes,
            COALESCE(SUM(i.watch_duration_seconds), 0) AS tempo_total,
            ROUND(COUNT(i.id_interacao) * @peso_interacoes + COALESCE(SUM(i.watch_duration_seconds), 0) * @peso_tempo) AS pontuacao
        FROM Conteudo c
        JOIN ConteudoCategoria cc ON c.id_conteudo = cc.id_conteudo
        JOIN Categoria cat ON cc.id_categoria = cat.id_categoria
        LEFT JOIN Interacao i ON c.id_conteudo = i.id_conteudo
        WHERE LOWER(cat.nome_categoria) = LOWER(@categoria)
        GROUP BY c.id_conteudo, c.nome_conteudo
        ORDER BY pontuacao DESC
        LIMIT 5
    ) AS categoria
)

UNION ALL

-- Parte 2: Top 5 conteúdos de outras categorias
(
    SELECT *
    FROM (
        SELECT
            c.id_conteudo,
            c.nome_conteudo,
            GROUP_CONCAT(DISTINCT cat.nome_categoria) AS categorias,
            COUNT(i.id_interacao) AS total_interacoes,
            COALESCE(SUM(i.watch_duration_seconds), 0) AS tempo_total,
            ROUND(COUNT(i.id_interacao) * @peso_interacoes + COALESCE(SUM(i.watch_duration_seconds), 0) * @peso_tempo) AS pontuacao
        FROM Conteudo c
        JOIN ConteudoCategoria cc ON c.id_conteudo = cc.id_conteudo
        JOIN Categoria cat ON cc.id_categoria = cat.id_categoria
        LEFT JOIN Interacao i ON c.id_conteudo = i.id_conteudo
        WHERE c.id_conteudo NOT IN (
            SELECT cc1.id_conteudo
            FROM ConteudoCategoria cc1
            JOIN Categoria cat1 ON cc1.id_categoria = cat1.id_categoria
            WHERE LOWER(cat1.nome_categoria) = LOWER(@categoria)
        )
        GROUP BY c.id_conteudo, c.nome_conteudo
        ORDER BY pontuacao DESC
        LIMIT 5
    ) AS outras
);

-- Gerar Distribuição de Tipos de Interação por Plataforma
SELECT p.id_plataforma, p.nome_plataforma, i.tipo_interacao, COUNT(*) AS total
FROM Interacao i
JOIN Plataforma p ON i.id_plataforma = p.id_plataforma
GROUP BY p.id_plataforma, p.nome_plataforma, i.tipo_interacao
ORDER BY p.nome_plataforma;

-- Gerar Relatório de Engajamento por Categoria
SELECT cat.nome_categoria,
       COUNT(i.id_interacao) AS total_interacoes,
       SUM(i.watch_duration_seconds) AS tempo_total
FROM Categoria cat
JOIN ConteudoCategoria cc ON cat.id_categoria = cc.id_categoria
JOIN Conteudo c ON c.id_conteudo = cc.id_conteudo
LEFT JOIN Interacao i ON i.id_conteudo = c.id_conteudo
GROUP BY cat.nome_categoria
ORDER BY total_interacoes DESC;

-- Horário de pico de engajamento
SELECT HOUR(timestamp_interacao) AS hora, COUNT(*) AS total
FROM Interacao
GROUP BY hora
ORDER BY total DESC
LIMIT 2;

-- Listar Conteúdos Agrupados por Categoria
SELECT cat.nome_categoria, GROUP_CONCAT(DISTINCT c.nome_conteudo SEPARATOR ', ') AS conteudos
FROM ConteudoCategoria cc
JOIN Conteudo c ON cc.id_conteudo = c.id_conteudo
JOIN Categoria cat ON cc.id_categoria = cat.id_categoria
GROUP BY cat.nome_categoria;

-- Gerar Relatório de Conteúdos Consumidos por Horário
SELECT c.nome_conteudo, HOUR(i.timestamp_interacao) AS hora, COUNT(*) AS interacoes
FROM Interacao i
JOIN Conteudo c ON i.id_conteudo = c.id_conteudo
GROUP BY c.nome_conteudo, hora
ORDER BY c.nome_conteudo, hora;