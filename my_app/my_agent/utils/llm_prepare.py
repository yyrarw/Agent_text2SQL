from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model

class LLMManager:
    def __init__(self, url):
        self.llm = init_chat_model("gpt-4o-mini")
        self.url = url

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content
    
    def structured(self, strc):
        return self.llm.with_structured_output(strc)