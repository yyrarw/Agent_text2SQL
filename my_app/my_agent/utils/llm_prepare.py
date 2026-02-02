from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class LLMManager:
    def __init__(self, url):
        self.llm = ChatOpenAI(
            model='tngtech/deepseek-r1t2-chimera:free',
            openai_api_key="",
            openai_api_base="https://openrouter.ai/api/v1",
            temperature=0.2
        )
        self.url = url

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content
    
    def structured(self, strc):
        return self.llm.with_structured_output(strc, method="json_mode", include_raw=True)