
from fastapi import HTTPException, Request
import fastapi
from fastapi.datastructures import Headers
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.dependencies import get_db

from starlette.middleware.base import BaseHTTPMiddleware
from utils.access_auth_baerer import decodeJWT
from sqlalchemy.orm import Session
from models.models import AuthData, Login
from database.database import SessionLocal

class MyMiddleware(BaseHTTPMiddleware):
    def __init__(
            self,
            app,
            
    ):
        super().__init__(app)
    

    async def dispatch(self, request: Request, call_next):
         
          
    
        
            url=str(request.url)
            
            if url.endswith("/login/") or url.endswith("/openapi.json") or url.endswith("/docs") or url.endswith("/register/") or url.endswith("gmail.com") :
                
               
                response = await call_next(request)
                return response
            else:
               
                authorization_header = request.headers.get('Authorization')
                if not authorization_header:
                    print(url)
                    return JSONResponse(status_code=200, content={"message": "Header is Missing"}) 
                else:
                   
                    token=authorization_header.rsplit()[1]
                    decoded_token=decodeJWT(token)
                    
                   
                    if decoded_token is None:
                        return JSONResponse(status_code=200, content={"message": "JWT Token is Invalid or Expired."})

                    else:
                       
                     
                        headers = dict(request.scope['headers'])
                        headers[b'user_id'] = str(decoded_token).encode()
                        request.scope['headers'] = [(k, v) for k, v in headers.items()]
                       
                        response = await call_next(request)
                     
                       
            
                        return response

                
          
            
          