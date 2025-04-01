# SQL para criar a tabela 'contratos' se ela não existir.
CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS contratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL NOT NULL,
    data_inicio TEXT NOT NULL,
    data_fim TEXT NOT NULL,
    requisitos TEXT NOT NULL
)
'''

# SQL para inserir um novo contrato.
INSERT_CONTRATO = '''
INSERT INTO contratos (valor, data_inicio, data_fim, requisitos)
VALUES (?, ?, ?, ?)
'''

# SQL para selecionar um contrato específico pelo seu ID.
SELECT_CONTRATO = '''
SELECT id, valor, data_inicio, data_fim, requisitos
FROM contratos
WHERE id = ?
'''

# SQL para selecionar todos os contratos da tabela.
SELECT_TODOS_CONTRATOS = '''
SELECT id, valor, data_inicio, data_fim, requisitos
FROM contratos
'''

# SQL para atualizar os dados de um contrato existente, identificado pelo ID.
UPDATE_CONTRATO = '''
UPDATE contratos
SET valor = ?, data_inicio = ?, data_fim = ?, requisitos = ?
WHERE id = ?
'''

# SQL para excluir um contrato da tabela, identificado pelo ID.
DELETE_CONTRATO = '''
DELETE FROM contratos
WHERE id = ?
'''
