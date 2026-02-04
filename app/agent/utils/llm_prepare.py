from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from config import Config

class LLMManager:
    def __init__(self, url):
        self.llm = ChatOpenAI(
            model=Config.OPENAI_MODEL,
            openai_api_key=Config.OPENAI_API_KEY,
            openai_api_base=Config.OPENAI_BASE_URL,
            temperature=Config.OPENAI_TEMPERATURE
        )
        self.url = url

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content
    
    def structured(self, strc):
        return self.llm.with_structured_output(strc, method="json_mode", include_raw=True)