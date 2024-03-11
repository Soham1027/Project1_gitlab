from fastapi import APIRouter,Depends, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi_mail import FastMail, MessageSchema, MessageType
from sqlalchemy.orm import Session
from utils.access_auth_baerer import AccessToken

from utils.reset_auth_baerer import RefreshToken
from auth import schemas
from utils.utils import get_hashed_password, verify_password
from service import service_auth
from database import dependencies
from models import models
router = APIRouter()

templates = Jinja2Templates(directory="templates")


###################################################################################################
#                                       REGISTER USER                                             #
###################################################################################################
 
    
@router.post("/register/", response_model=dict,tags=['Authentication'])
def user_registration(users: schemas.UserCreate, db: Session = Depends(dependencies.get_db)):
   
    user_register= service_auth.register(db,users)
    
    if user_register:
      
       return jsonable_encoder(user_register)
    else:
         return JSONResponse(status_code=400, content={"error":"Invalid data credentials"})
     
     
###################################################################################################
#                                       LOGIN USER                                                #
###################################################################################################


@router.post("/login/", response_model=dict, tags=['Authentication'])
def user_login(credentials: schemas.UserLogin, db: Session = Depends(dependencies.get_db)):
    user_info = service_auth.login(db, credentials)

    if user_info:
       
        return jsonable_encoder(user_info)
    else:
          return JSONResponse(status_code=400, content={"error":"Invalid data credentials"})

 
    
###################################################################################################
#                                       CHANGE PASSWORD                                           #
###################################################################################################


@router.post("/change-password/",tags=['Authentication'])
def change_password(request: schemas.changepassword,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())): # type: ignore
   # data=(decode_email_token(refresh_token))
   

    password = service_auth.user_change_password(db, request)

    return {"message": "Password changed successfully"}



###################################################################################################
#                                       FORGOT PASSWORD                                           #
###################################################################################################

@router.post("/reset_password/", response_model=dict, tags=['Authentication'])
def reset_password(request:Request,reset_credentials: schemas.PasswordReset, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
   
    user_info = service_auth.user_reset_password(db,request, reset_credentials)

    if user_info:
       
        return jsonable_encoder(user_info)
    else:
         return JSONResponse(status_code=400, content={"error":"Invalid data credentials"})

  
###################################################################################################
#                                      SEND RESET PASSWORD EMAIL                                  #
###################################################################################################

 
  
@router.post("/send_email_reset_password/",tags=['Authentication'])
def reset_password_email(email:str,db: Session = Depends(dependencies.get_db)): # type: ignore
  
      
        user=db.query(models.AuthData).filter_by(email=email).first()
       
        if user:
            if service_auth.send_reset_password_email(db,email):
              return{"message":"sent mail"}
            else:
                return JSONResponse(status_code=400,content={"error":"Fail to Send Email"})
        else:
                return JSONResponse(status_code=400,content={"error":"Invalid data credentials"})

  
###################################################################################################
#                                       LOGOUT USER                                               #
###################################################################################################

  
  
@router.delete("/logout/",tags=['Authentication'])
def logout_user(logout_request: schemas.UserLogout, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    logout = service_auth.logout_user(db, logout_request) # type: ignore

    return {"message": "User Logout successfully"}


###################################################################################################
#                                       RESET ACCESS TOKEN                                        #
###################################################################################################


@router.post("/reset_user_access_token/",tags=['Authentication'])
def reset_user_access_token(reset_acceess_token:schemas.ResetAccessTokenCreate,db: Session = Depends(dependencies.get_db),dependencies=Depends(RefreshToken())): # type: ignore
  reset_user_access_token=service_auth.reset_acceess_token(db,reset_acceess_token)

  return reset_user_access_token