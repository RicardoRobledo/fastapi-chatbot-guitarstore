from fastapi import APIRouter
from ... import config


router = APIRouter(prefix='/conversation', tags=['Conversation'])

@router.post('/cleaner-manager')
async def delete_conversation():
    return {'message': 'deleted'}
