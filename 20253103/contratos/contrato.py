from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date

class Contrato(BaseModel):
    id: Optional[int] = None
    valor: float
    data_inicio: date
    data_fim: date
    requisitos: str

    @field_validator('id')
    def validar_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError('O id do contrato não pode ser negativo ou zero.')
        return v

    @field_validator('valor')
    def validar_valor(cls, v):
        if v <= 0:
            raise ValueError('O valor do contrato deve ser maior que zero.')
        return v

    @field_validator('data_inicio')
    def validar_data_inicio(cls, v):
        if not isinstance(v, date):
            raise ValueError('A data de início deve ser uma data válida.')
        return v

    @field_validator('data_fim')
    def validar_data_fim(cls, v):
        if not isinstance(v, date):
            raise ValueError('A data de fim deve ser uma data válida.')
        return v
    
    @field_validator('requisitos')
    def validar_requisitos(cls, v):
        requisitos_limpos = v.strip()
        if not requisitos_limpos:
            raise ValueError('Os requisitos do contrato não podem ser vazios.')
        if len(requisitos_limpos) > 500:
            raise ValueError('Os requisitos do contrato não podem exceder 500 caracteres.')
        return requisitos_limpos
