from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth_sheme = OAuth2PasswordBearer(tokenUrl='token')

@app.post('/token')
async def gen_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token':form_data.username+'token'}

@app.get('/')
async def index(token:str = Depends(oauth_sheme)):
    return {'the_token':token} 




