from fastapi.encoders import jsonable_encoder
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_REFESH_SECRET_KEY="439340ce06dca59e096161c2ca1f45f7d64ec962d6fd78dd082686cbc91c36b9"
JWT_SECRET_KEY = "9c435539b8c08a31ce1c93bf797abcb1c5c3993824be18568b7b5aba40456c04"
def decodeJWT(jwtoken: str):
   
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM) # type: ignore
        for i in payload:
            if i=="sub":
                data_payload=payload[i]
                print("payload",data_payload)
                
                return data_payload
                
              
            else:
                    
                return None
        
        
    
    except InvalidTokenError:
        return None



class AccessToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(AccessToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        reset_credentials: HTTPAuthorizationCredentials = await super(AccessToken, self).__call__(request) # type: ignore
        if reset_credentials:
            if not reset_credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(reset_credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return reset_credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

jwt_bearer = AccessToken()