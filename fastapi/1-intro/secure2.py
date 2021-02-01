from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordRequestForm
from fastapi.security.oauth2 import OAuth2PasswordBearer 
from tortoise.models import Model 
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.contrib.fastapi import register_tortoise
from passlib.hash import bcrypt
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta

JWT_SECRET = '0e5ffbe37d49fd01bfcc95f50480b3efaac6ae31c3310bd121604b30f2d76266'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
app = FastAPI()
 
class Token(BaseModel):
    access_token: str
    token_type: str 

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50,unique=True)
    password_hash = fields.CharField(128)
       
    def verify_password(self,password):
        return bcrypt.verify(password,self.password_hash)
    
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)   

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

async def authenticate_user(username : str, password : str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.post('/token', response_model=Token)
async def generate_token(form_data : OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    to_encode = user_obj.dict()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire_time})
    access_token = jwt.encode(to_encode, JWT_SECRET, algorithm = ALGORITHM)
    return {'access_token':access_token, 'token_type':'bearer'}
    
    
@app.post('/users',response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

async def get_current_user(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return await User_Pydantic.from_tortoise_orm(user)

@app.get('/users/me', response_model=User_Pydantic)
async def get_user(user : User_Pydantic = Depends(get_current_user)):
    return user

register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules = {'models':['secure2']},
    generate_schemas=True,
    add_exception_handlers=True
)

