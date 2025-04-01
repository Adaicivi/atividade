from typing import List, Optional
from contratos.contrato import Contrato
from contratos import contrato_sql as sql
from util import get_db_connection
import sqlite3

class ContratoRepo:
    def __init__(self):
        self._criar_tabela()

    def _criar_tabela(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.CREATE_TABLE)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def adicionar(self, contrato: Contrato) -> Optional[int]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.INSERT_CONTRATO, (contrato.valor, contrato.data_inicio, contrato.data_fim, contrato.requisitos))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao adicionar contrato: {e}")
            return None

    def obter(self, contrato_id: int) -> Optional[Contrato]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_CONTRATO, (contrato_id,))
                row = cursor.fetchone()
                if row:
                    return Contrato(id=row[0], valor=row[1], data_inicio=row[2], data_fim=row[3], requisitos=row[4])
                return None
        except sqlite3.Error as e:
            print(f"Erro ao obter contrato {contrato_id}: {e}")
            return None

    def obter_todos(self) -> List[Contrato]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_TODOS_CONTRATOS)
                rows = cursor.fetchall()
                return [Contrato(id=row[0], valor=row[1], data_inicio=row[2], data_fim=row[3], requisitos=row[4]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao obter todos os contratos: {e}")
            return []

    def atualizar(self, contrato: Contrato) -> bool:
        if contrato.id is None:
            print("Erro: Contrato sem ID não pode ser atualizado.")
            return False
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.UPDATE_CONTRATO, (contrato.valor, contrato.data_inicio, contrato.data_fim, contrato.requisitos, contrato.id))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar contrato {contrato.id}: {e}")
            return False

    def excluir(self, contrato_id: int) -> bool:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.DELETE_CONTRATO, (contrato_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir contrato {contrato_id}: {e}")
            return False
