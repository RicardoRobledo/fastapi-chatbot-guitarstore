from ..desing_patterns.creational_patterns.singleton.gemini_singleton import GeminiSingleton
from ..desing_patterns.creational_patterns.singleton.chromadb_singleton import ChromaSingleton
from ..logical_routers.routers import ClassifierRouter, DatabaseRouter
from ..tools.chatbot_tools import ChromaTool, DatabaseTool, VeracityTool

from ..utils.prompt_handlers.prompt_loader import load_prompt_file

from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

import json


class ChatbotRepository():


    async def post_user_message(self, message):

        GeminiSingleton()
        ChromaSingleton()

        classifier_result = await ClassifierRouter().route(message)

        if classifier_result['structured_output']['herramienta']=='Veracity':

            msg = await VeracityTool()._arun(message)
            print('Veracity')

        else:

            database_result = await DatabaseRouter().route(message)

            if database_result['structured_output']['herramienta']=='ChromaDB':
                msg = await ChromaTool()._arun(message)
                print('ChromaDB')

            elif database_result['structured_output']['herramienta']=='SQLDatabase':
                msg = await DatabaseTool()._arun(message)
                print('Database')

        return msg
