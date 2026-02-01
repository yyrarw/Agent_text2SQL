from data_prepare import DataBaseManager
from llm_prepare import LLMManager
from state import ChooseTable, ChooseTableColumns, ValidSQL, CheckSQL
from prompts import CHOISE_TABLE_PROMPT, CHOISE_TABLE_AND_COLUMNS_PROMPT, VALIDATE_SQL, CHECK_SQL, ANSWER


class AgentTools:
    def __init__(self, db_id, url):
        self.llm_manager = LLMManager(url)
        self.db_manager = DataBaseManager(db_id)
        self.schema = self.db_manager.get_schema()
        
    def choice_table(self, state):
        question = state['question']
        structure = ChooseTable
        structured_llm = self.llm_manager.structured(structure)
        prompt = CHOISE_TABLE_PROMPT
        chain = prompt | structured_llm
        
        try:
            table = chain.invoke({
                'question': question,
                'schema': self.schema
            })
            
            if table.is_relevant_tables:
                print('------------------------AIMassage------------------------\n')
                print(table.explanation)
                
                return {'relevant_tables': table.relevant_tables}
            
            else:
                print('В базе данных нет подходящей информации:', table.explanation)
                return {'error': 'TableError'}
            
        except Exception as e:
            print(f'Ошибка структурированного вывода, попробуйте использовать модель, поддерживающую ToosCallings и StructuredOutput:\n{e}')
            return {'error': 'ModelErorr', 'relevant_tables': {}} 
    
    def choise_columns(self, state):
        question = state['question']
        structure = ChooseTableColumns
        structured_llm = self.llm_manager.structured(structure)
        
        prompt = CHOISE_TABLE_AND_COLUMNS_PROMPT
        
        table_with_columns = structured_llm.invoke(
            prompt=prompt,
            question=question,
            schema=state['relevant_tables']
        )
        
        print('------------------------AIMassage------------------------\n')
        print(table_with_columns.explanation)
        
        return {'relevant_tables_with_rel_columns': table_with_columns.relevant_tables_with_rel_columns}
    
    def generate_sql(self, state):
        question = state['question']
        structure = ValidSQL
        structured_llm = self.llm_manager.structured(structure)
        prompt = VALIDATE_SQL
        
        if not state['used_stop_words']:
            sql_response = structured_llm.invoke(
                prompt=prompt,
                question=question,
                sql_error_info=state.get('sql_error_info', ''),
                stop_words = '',
                schema=state['relevant_tables_with_rel_columns']
            )
            
        else:
            sql_response = structured_llm.invoke(
                prompt=prompt,
                question=question,
                sql_error_info=state['sql_error_info'],
                stop_words=f" Не используй {state['used_stop_words']}\n\n",
                schema=state['relevant_tables_with_rel_columns']
            )
            
        print('------------------------AIMassage------------------------\n')
        print(sql_response.explanation)
            
        return {'sql_request': sql_response.sql_request, 'sql_generate_count': state.get('sql_generate_count', 0) + 1}
            
    
    
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
        structure = CheckSQL
        structured_llm = self.llm_manager.structured(structure)
        prompt = CHECK_SQL
        
        checked_sql = structured_llm.invoke(
            prompt=prompt,
            question=question,
            schema=state['relevant_tables_with_rel_columns']
        )
        
        if checked_sql.sql_request_is_valid:
            return {'sql_request_is_valid' : checked_sql.sql_request_is_valid}
        
        else:
            return {'sql_request_is_valid' : checked_sql.sql_request_is_valid, 'sql_error_info': checked_sql.explanation}
    
    def create_answer(self, state):
        question = state['question']
        prompt = ANSWER
        response = self.llm_manager.invoke(
            prompt=prompt,
            question=question,
            result=state['result']
        )
        
        return {'answer': response}
        