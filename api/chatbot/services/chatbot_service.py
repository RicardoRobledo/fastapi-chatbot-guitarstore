from ..repositories.chatbot_repository import ChatbotRepository 


class ChatbotService():

    async def post_user_message(self, message):

        return await ChatbotRepository().post_user_message(message)
