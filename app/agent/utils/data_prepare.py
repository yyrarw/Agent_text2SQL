import ast
import sqlite3
from pathlib import Path
from langchain_community.utilities import SQLDatabase

BASE_DIR = Path(__file__).resolve().parent.parent


class DataBaseManager:
    def __init__(self, uiid, base_dir=BASE_DIR):
        self.db_path =  base_dir  / 'data'  / "sqlite_db" / f"{uiid}.db"                  # Путь к файлу с БД
        self.sql_path = base_dir  / 'data'  / "databases" / f"database_{uiid}_full.sql"   # Путь к файлу SQL скрипта
        
        self._prepare_data()                                                              # Инициализация функции
        self.db = SQLDatabase.from_uri(f'sqlite:///{self.db_path}')                       # Создание объекта SQLDatabase
        
    def _prepare_data(self):
        '''
        Создаёт БД из SQL-скрипта, если она не существует.
        
        param db_path: Путь к файлу, в который будет сохранена database
        type db_path: str
        
        param sql_path: Путь к файлу формата .sql из которого беруться данные
        type sql_path: str
        '''
        
        if not self.db_path.exists():       # Создает БД, если она не создана
            
            if not self.sql_path.exists():
                raise FileNotFoundError(f"SQL не найден: {self.sql_path}")
            
            conn = sqlite3.connect(self.db_path) # Подключается к БД

            with open(self.sql_path, 'r') as sql_file:
                sql_script = sql_file.read()
                
            conn.executescript(sql_script)  # Выполняет все SQL запросы из sql_script
            conn.commit()                   # Записывает данные на диск
            conn.close()                    # Закрывает БД
            
            print('Database создана!')
        else:
            print('Database уже была создана!')
     
    def get_schema(self):
        table_names = self.db.get_usable_table_names()
        db_describe = {}
        
        for table_name in table_names:
            temp_describe = ast.literal_eval(self.db.run(f'PRAGMA table_info({table_name});'))
            temp_table_name = [f'column={name[1]}, type={name[2]}' for name in temp_describe]
            db_describe[table_name] = temp_table_name
            
        return db_describe
    
    def execute_query(self, query):
        return self.db.run(f'{query}')
    
    
    
# temp = DataBaseManager('banking')

# print(temp.get_schema())



