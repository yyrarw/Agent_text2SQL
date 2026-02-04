from .data_prepare import DataBaseManager
from .llm_prepare import LLMManager
from .state import ChooseTable, ChooseTableColumns, ValidSQL, CheckSQL
from .prompts import CHOISE_TABLE_PROMPT, CHOISE_TABLE_AND_COLUMNS_PROMPT, VALIDATE_SQL, CHECK_SQL, ANSWER
from langchain_core.output_parsers.json import JsonOutputParser



class AgentTools:
    def __init__(self, db_id, url):
        self.llm_manager = LLMManager(url)
        self.db_manager = DataBaseManager(db_id)
        self.schema = self.db_manager.get_schema()
        
    def choice_table(self, state):
        question = state['question']
        parser = JsonOutputParser(pydantic_object=ChooseTable)
        chain = CHOISE_TABLE_PROMPT | self.llm_manager.llm | parser
        
        try:
            table = chain.invoke({
                'question': question,
                'schema': self.schema
            })
            
            if table.get('is_relevant_tables', False):
                print('------------------------AIMassage------------------------\n')
                print(table.get('explanation', ''))
                
                return {'relevant_tables': table.get('relevant_tables', {})}
            
            else:
                print('В базе данных нет подходящей информации:', table.get('explanation', ''))
                return {'error': 'TableError', 'table_counter': state.get('table_counter', 0)}
            
        except Exception as e:
            print(f'Ошибка структурированного вывода, попробуйте использовать модель, поддерживающую ToosCallings и StructuredOutput:\n{e}')
            return {'error': 'ModelErorr', 'relevant_tables': {}} 
        
    def tables_samples(self, state):
        tables = state.get('relevant_tables')
        tables_info = {}
        for table in tables.keys():
            query = f"SELECT * FROM {table} LIMIT 5"
            table_info = self.db_manager.execute_query(query)
            tables_info[table] = table_info
        return {'tables_info': tables_info}
    
    def choise_columns(self, state):
        question = state['question']
        parser = JsonOutputParser(pydantic_object=ChooseTableColumns)
        
        chain = CHOISE_TABLE_AND_COLUMNS_PROMPT | self.llm_manager.llm | parser
        
        table_with_columns = chain.invoke({
            'question': question,
            'schema': state['relevant_tables'],
            'tables_info': state['tables_info']
        })
        
        print('------------------------AIMassage------------------------\n')
        print(table_with_columns.get('explanation', ''))
        
        return {'relevant_tables_with_rel_columns': table_with_columns.get('relevant_tables_with_rel_columns', {})}
    
    def generate_sql(self, state):
        question = state['question']
        parser = JsonOutputParser(pydantic_object=ValidSQL)
        
        chain = VALIDATE_SQL | self.llm_manager.llm | parser
        
        if not state.get('used_stop_words'):
            sql_response = chain.invoke({
                'question': question,
                'sql_error_info': state.get('sql_error_info', ''),
                'stop_words': '',
                'schema': state['relevant_tables_with_rel_columns'],
                'tables_info': state['tables_info']
            })
            
        else:
            sql_response = chain.invoke({
                'question': question,
                'sql_error_info': state['sql_error_info'],
                'stop_words': f" Не используй {state['used_stop_words']}\n\n",
                'schema': state['relevant_tables_with_rel_columns'],
                'tables_info': state['tables_info']
            })
            
        print('------------------------AIMassage------------------------\n')
        print(sql_response.get('explanation', ''))
            
        return {'sql_request': sql_response.get('sql_request', ''), 'sql_generate_count': state.get('sql_generate_count', 0)}
            
    
    
    def security_check(self, state):
        stop_words = {'DROP', 'ALTER', 'TRUNCATE', 'CREATE', 'DELETE', 'UPDATE', 'INSERT'}
        sql_upper = state['sql_request'].upper()
        
        detected = stop_words.intersection(sql_upper.split())
        if detected:
            return {
                'stop_words': True, 
                'used_stop_words': list(detected)
            }
        return {'stop_words': False}
    
    def execut_sql(self, state):
        try:
            query = state['sql_request']
            result = self.db_manager.execute_query(query)
            return {'result': result, 'sql_request_is_valid': True}
        
        except Exception as e:
            return {'sql_request_is_valid': False, 'sql_error_info': f'{e}'}
    
    def validate_sql(self, state):
        question = state['question']
        
        parser = JsonOutputParser(pydantic_object=CheckSQL)
        chain = CHECK_SQL | self.llm_manager.llm | parser
        
        checked_sql = chain.invoke({
            'schema': state['relevant_tables_with_rel_columns'],
            'sql_request': state['sql_request'],
            'sql_error_info': state['sql_error_info'],
            'tables_info': state['tables_info']
        })
        
        if checked_sql.get('sql_request_is_valid'):
            return {'sql_request_is_valid' : checked_sql.get('sql_request_is_valid', False)}
        
        else:
            return {'sql_request_is_valid' : checked_sql.get('sql_request_is_valid', False), 'sql_error_info': checked_sql.get('explanation', '')}
    
    def create_answer(self, state):
        # question = state['question']
        # prompt = ANSWER
        # response = self.llm_manager.invoke(
        #     prompt=prompt,
        #     question=question,
        #     result=state['result']
        # )
        
        return {'answer': state['result']}
        