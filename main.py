import sys

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from api.chatbot.desing_patterns.creational_patterns.singleton.gemini_singleton import GeminiSingleton

import api


@asynccontextmanager
async def lifespan(app: FastAPI):
    print('startup')
    GeminiSingleton()

    yield
    print('shutdown')


app = FastAPI(
    title="Asistente de clientes",
    description="API para la asistencia de clientes",
    version="0.1",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api.router)


from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request


templates = Jinja2Templates(directory="frontend")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


@app.get("/frontend")
def read_root(request:Request):
    return templates.TemplateResponse('index.html', context={'request': request})


# -------------------------------------------


#from fastapi.templating import Jinja2Templates
#from fastapi.staticfiles import StaticFiles
#from fastapi.requests import Request


#templates = Jinja2Templates(directory="frontend/build")
#app.mount("/static", StaticFiles(directory="frontend/build/static"), name="static")


#@app.get("/admin")
#def read_root(request:Request):
#    return templates.TemplateResponse('index.html', context={'request': request})


#@app.get("/ej")
#def read_root(request:Request):
#    return {'s':'sd'}
