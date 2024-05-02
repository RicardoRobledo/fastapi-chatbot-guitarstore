from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import chromadb

from ..... import config


__author__ = 'Ricardo'
__version__ = '0.1'


class ChromaSingleton():

    __client = None
    __embedding = None


    @classmethod
    def __get_connection(self, embedding):
        """
        This method create our client
        """

        client = chromadb.PersistentClient(path="./chroma_db")
 
        return Chroma(client=client, collection_name="tienda_guitarras", embedding_function=embedding)
 

    def __new__(cls, *args, **kwargs):
        
        if cls.__client==None:
            cls.__embedding = GoogleGenerativeAIEmbeddings(model=config.MODEL_EMBEDDING)
            cls.__client = cls.__get_connection(cls.__embedding)

        return cls.__client


    @classmethod
    async def search_similarity_guitar(cls, text:str):
        """
        This method search the similarity in a text given inside Pinecone

        :param text: an string beging our text to query
        :return: a list with our documents 
        """

        docs = await cls.__client.asimilarity_search(text, k=5)
        
        return docs

