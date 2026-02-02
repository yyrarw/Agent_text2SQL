from langgraph.graph import StateGraph, START, END
from state import State
from tools import AgentTools

class WorkflowManager:
    def __init__(self, db_id, url):
        self.llm_manager = AgentTools(db_id, url)
        
    def fill_workflow(self):
        workflow = StateGraph(State)
        
        workflow.add_node('choice_table',   self.llm_manager.choice_table)
        workflow.add_node('tables_samples', self.llm_manager.tables_samples)
        workflow.add_node('choise_columns', self.llm_manager.choise_columns)
        workflow.add_node('generate_sql',   self.llm_manager.generate_sql)
        workflow.add_node('security_check', self.llm_manager.security_check)
        workflow.add_node('execut_sql',     self.llm_manager.execut_sql)
        workflow.add_node('validate_sql',   self.llm_manager.validate_sql)
        workflow.add_node('create_answer',  self.llm_manager.create_answer)
        
        workflow.add_edge(START, 'choice_table')
        workflow.add_conditional_edges('choice_table', self._relevant_table_edge, {
            'RetryTable': 'choice_table',
            'ChangeModel': END,
            'Continue': 'tables_samples',
            'MaxLimit': END
        })
        workflow.add_edge('tables_samples', 'choise_columns')
        workflow.add_edge('choise_columns', 'generate_sql')
        workflow.add_edge('generate_sql', 'security_check')
        workflow.add_conditional_edges('security_check', self._security_check, {
            'generate_sql': 'generate_sql',
            'execut_sql': 'execut_sql'
        })
        workflow.add_conditional_edges('execut_sql', self._sql_check, {
            'create_answer': 'create_answer',
            'validate_sql': 'validate_sql'
        })
        workflow.add_conditional_edges('validate_sql', self._valid_check, {
            'execut_sql': 'execut_sql',
            'generate_sql': 'generate_sql',
            'MaxLimit': END
        })
        workflow.add_edge('create_answer', END)
        
        return workflow
        
    def _relevant_table_edge(self, state):
        count = state['table_counter']
        
        if count > 3:
            return 'MaxLimit'
        
        if state.get('error') == 'TableError':
            return 'RetryTable'
        
        elif state.get('error') == 'ModelErorr':
            return 'ChangeModel'
        
        else:
            return 'Continue'
        
    def _security_check(self, state):
        if state.get('stop_words'):
            return 'generate_sql'
        
        else:
            return 'execut_sql'
        
    def _sql_check(self, state):
        if state.get('sql_request_is_valid'):
            return 'create_answer'
        
        else:
            return 'validate_sql'
        
    def _valid_check(self, state):
        count = state.get('sql_generate_count')
        
        if count > 3:
            return 'MaxLimit'
        
        if state.get('sql_request_is_valid'):
            return 'execut_sql'
        
        else:
            return 'generate_sql'
        
        
    def return_graph(self):
        return self.fill_workflow().compile()
        
        
            
        
        
        