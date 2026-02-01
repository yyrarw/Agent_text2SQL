from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class LLMManager:
    def __init__(self, url):
        self.llm = ChatOpenAI(
            base_url=f"http://{url}/v1",
            api_key='lm-studio'
        )

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content
    
    def structured(self, strc):
        return self.llm.with_structured_output(strc)