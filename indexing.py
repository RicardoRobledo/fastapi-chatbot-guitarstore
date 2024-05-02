import os
import chromadb
import pandas as pd
from langchain_chroma import Chroma
from langchain_core.documents import Document
from api.config import GOOGLE_API_KEY

from langchain_google_genai import GoogleGenerativeAIEmbeddings


os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


persistent_client = chromadb.PersistentClient(path="./chroma_db")

docs = []

#df = pd.read_csv("preg-res-tiendaguitarras.csv")
#for i, j in df[['preguntas', 'respuestas']].values:
#    docs.append(Document(
#        page_content=i,
#        metadata={'answer':j}
#    ))

#persistent_client.get_or_create_collection("tienda_guitarras")

#langchain_chroma = Chroma.from_documents(
#    documents=docs,
#    client=persistent_client,
#    collection_name="tienda_guitarras",
#    embedding=embedding,
#)

db3 = Chroma(client=persistent_client, collection_name="tienda_guitarras", embedding_function=embedding)
docs = db3.similarity_search('precio', k=5)
print(docs)
