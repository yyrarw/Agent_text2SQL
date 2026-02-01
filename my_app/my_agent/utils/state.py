from typing_extensions import TypedDict
from typing import Dict, List, Optional, Literal, Annotated
from pydantic import BaseModel, Field
from operator import add


class State(TypedDict):
    question: str
    table_error_info: Optional[str]
    table_counter: Annotated[int, add]
    sql_generate_count: Annotated[int, add]
    relevant_tables: Dict[str, List[str]]
    relevant_tables_with_rel_columns: Dict[str, List[str]]
    sql_request: str
    sql_request_is_valid: bool
    sql_error_info: Optional[str]
    stop_words: bool
    used_stop_words: List[str]
    error: Optional[str]
    result: Optional[str]
    answer: Optional[str]
    
    
    
class ChooseTable(BaseModel):
    relevant_tables: Dict[str, List[str]] = Field(
        ...,
        description="Словарь с ключами - названиями релевантных таблиц, значениями - списками колонок в этой таблице"
    )
    
    is_relevant_tables: bool = Field(
        ...,
        description="True если нашел релевантные таблицы, иначе False"
    )
    
    explanation: str = Field(
        ...,
        description="Если is_relevant_tables is True кратко объянени (1 предложение) выбор таблиц, иначе кратко напиши в чем проблема"
    )
    
    
class ChooseTableColumns(BaseModel):
    relevant_tables_with_rel_columns: Dict[str, List[str]] = Field(
        ...,
        description="Словарь с ключами - названиями таблиц, значениями - списками релевантных колонок в этой таблице"
    )
    
    explanation: str = Field(
        ...,
        description="Почему выбраны эти колонки (1 предложение)"
    )
    
    
class ValidSQL(BaseModel):
    sql_request: str = Field(
        ...,
        description="Валидный SQL-запрос для ответа на вопрос."
    )
    
    explanation: str = Field(
        default='',
        description="Логика SQL запроса."
    )
    

class CheckSQL(BaseModel):
    sql_request_is_valid: Literal[True, False] = Field(
        ...,
        description="True если SQL синтаксически корректен, False иначе."
    
    ) 
    explanation: str = Field(
        default='',
        description="Проблемы SQL ИЛИ подтверждение корректности"
    )
