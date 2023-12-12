from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    properties: dict 

class UserRequest(BaseModel):
    utterance: str
    callbackUrl: Optional[str] = None
    user: User

class Intent(BaseModel):
    name: str

class ChatbotRequest(BaseModel):
    userRequest: UserRequest
    intent: Intent
    action: dict


# {userRequest={utterance=안녕, callbackUrl=null, user={id=1234567890, properties={}}}, intent={name=hello}, action={params={}, id=hello, detailParams={}}} 
# {"userRequest"={"utterance"="안녕", "callbackUrl"=null, "user"={"id"="1234567890", "properties"={}}}, "intent"={"name"="hello"}, "action"={"params"={}, "id"="hello", "detailParams"={}}}
# {""}
