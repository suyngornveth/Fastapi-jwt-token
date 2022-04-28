from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from schemas import AuthDetails
import uvicorn


app = FastAPI()

auth_handler = AuthHandler()
users = []


@app.post('/register')
def register(auth_detail: AuthDetails):
    if any(x['username'] == auth_detail.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_detail.password)
    users.append({
        'username': auth_detail.username,
        'password': hashed_password
    })
    return


@app.post('/login')
def login(auth_detail: AuthDetails):
    user = None
    for x in users:
        if x in users:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_detail.password, user['password'])):
        raise HTTPException(status_code=401, detail="Invalid username and password")
    token = auth_handler.endcode_token(user['username'])
    return{
        'token': token
    }
            

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get('/me')
def me(username=Depends(auth_handler.auth_wrapper)):
    return {
        'name': username
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8001, reload=True)