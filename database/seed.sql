-- ============================================================
-- SEED - Sistema de Gerenciamento de Laboratórios
-- Dados básicos para desenvolvimento e demonstração
-- ============================================================

-- ============================================================
-- USUÁRIO
-- ============================================================

INSERT INTO usuario (
    "nome",
    "email",
    "tipo",
    "senha"
)
VALUES (
    'Funcionário TI Demo',
    'demo@instituicao.com',
    'Funcionário de TI',
    '123456'
)
ON CONFLICT ("email") DO NOTHING;


-- ============================================================
-- PROFESSOR
-- ============================================================

INSERT INTO professor (
    "nome",
    "email",
    "matricula"
)
VALUES (
    'Professor Demo',
    'professor.demo@instituicao.com',
    'PROF-DEMO-001'
)
ON CONFLICT ("email") DO NOTHING;


-- ============================================================
-- LABORATÓRIOS
-- ============================================================

INSERT INTO laboratorio (
    "nome",
    "localizacao",
    "capacidade",
    "status"
)
VALUES
(
    'Laboratório Demo 01',
    'Bloco A - Sala 101',
    30,
    'Ativo'
),
(
    'Laboratório Demo 02',
    'Bloco B - Sala 202',
    30,
    'Ativo'
)
ON CONFLICT ("nome") DO NOTHING;


-- ============================================================
-- COMPUTADORES
-- ============================================================

INSERT INTO computador (
    "patrimonio",
    "especificacao",
    "status",
    "idLaboratorio"
)
SELECT
    'PC-DEMO-001',
    'Computador para demonstração',
    'Disponível',
    l."idLaboratorio"
FROM laboratorio l
WHERE l."nome" = 'Laboratório Demo 01'
AND NOT EXISTS (
    SELECT 1
    FROM computador c
    WHERE c."patrimonio" = 'PC-DEMO-001'
);


INSERT INTO computador (
    "patrimonio",
    "especificacao",
    "status",
    "idLaboratorio"
)
SELECT
    'PC-DEMO-002',
    'Computador para demonstração',
    'Disponível',
    l."idLaboratorio"
FROM laboratorio l
WHERE l."nome" = 'Laboratório Demo 01'
AND NOT EXISTS (
    SELECT 1
    FROM computador c
    WHERE c."patrimonio" = 'PC-DEMO-002'
);


-- ============================================================
-- AULA
-- ============================================================

INSERT INTO aula (
    "disciplina",
    "data",
    "horaInicio",
    "horaFim",
    "idProfessor",
    "idLaboratorio"
)
SELECT
    'Aula de Demonstração',
    '2026-10-20',
    '08:00:00',
    '10:00:00',
    p."idProfessor",
    l."idLaboratorio"
FROM professor p
CROSS JOIN laboratorio l
WHERE p."email" = 'professor.demo@instituicao.com'
AND l."nome" = 'Laboratório Demo 01'
AND NOT EXISTS (
    SELECT 1
    FROM aula a
    WHERE a."disciplina" = 'Aula de Demonstração'
    AND a."data" = '2026-10-20'
    AND a."idLaboratorio" = l."idLaboratorio"
);


-- ============================================================
-- MANUTENÇÃO
-- ============================================================

INSERT INTO manutencao (
    "dataInicio",
    "dataFim",
    "motivo",
    "status",
    "idLaboratorio"
)
SELECT
    '2026-10-21',
    '2026-10-22',
    'Manutenção programada para demonstração',
    'Ativa',
    l."idLaboratorio"
FROM laboratorio l
WHERE l."nome" = 'Laboratório Demo 01'
AND NOT EXISTS (
    SELECT 1
    FROM manutencao m
    WHERE m."motivo" = 'Manutenção programada para demonstração'
    AND m."idLaboratorio" = l."idLaboratorio"
);