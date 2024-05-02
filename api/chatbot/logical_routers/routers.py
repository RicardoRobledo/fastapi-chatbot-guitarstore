import json

from ..utils.prompt_handlers.prompt_loader import load_prompt_file
from ..desing_patterns.creational_patterns.singleton.gemini_singleton import GeminiSingleton

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


__author__ = 'Ricardo'
__version__ = '0.1'


class BaseRouter():

    async def route(self, message:str, prompt_path:str) -> str:
        
        prompt = load_prompt_file(prompt_path)

        chat_template = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(prompt)
        ])

        formatted_chat_template = chat_template.format_messages(message=message)
        ia = await GeminiSingleton.post_user_message(formatted_chat_template)
        ia_structured_output = json.loads(ia)

        return {'structured_output': ia_structured_output,
                'memory': f"razon: {ia_structured_output['razon']} - herramienta{ia_structured_output['herramienta']}"}



class ClassifierRouter(BaseRouter):
    """
    This class route our message
    """

    async def route(self, message:str) -> str:
        return await super().route(message, "api/chatbot/prompts/classifier_prompt.txt")


class DatabaseRouter(BaseRouter):
    """
    This class route our message in a database (sql or vectorial)
    """

    async def route(self, message:str) -> str:
        return await super().route(message, "api/chatbot/prompts/router_prompt.txt")
