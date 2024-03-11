from fastapi import HTTPException, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import jwt

from sqlalchemy.orm import Session
from datetime import timedelta,datetime, timezone


from models.models import AuthData, PasswordAndAccessResetToken,Login
from auth import schemas
from utils.connection_config import send_reset_email
from utils.utils import  create_reset_token ,get_hashed_password,create_jwt_token,verify_password
ACCESS_TOKEN_EXPIRE_MINUTES = 30 



###################################################################################################
#                                      REGISTER                                                   #
###################################################################################################

USER_LOGIN_DATA=[]

def register(db: Session, user: schemas.UserCreate): 
    expire_time= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_in=expire_time
    
    existing_email = db.query(AuthData).filter_by(email=user.email).first()
    existing_user = db.query(AuthData).filter_by(name=user.name).first()
   
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
   
    elif existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    password=get_hashed_password(user.password)
    token = create_jwt_token({"sub":user.email})
    refresh_token = create_reset_token(user.email)
    db_user = AuthData(name=user.name,email=user.email,token=token,refresh_token=refresh_token,expire_in=expire_in,role=user.role, password=password,updated_at=datetime.utcnow()) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    
    return {"message":"User is Register, Now you can Login."} 
    
   

###################################################################################################
#                                     LOGIN                                                       #
###################################################################################################


def login(db: Session ,credentials: schemas.UserLogin):
   
    expire_in= datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    user = db.query(AuthData).filter_by(email=credentials.email).first()
   
   
    if user and verify_password(credentials.password, user.password):# type: ignore
       
        token = create_jwt_token({"sub":user.id}) # type: ignore
        refresh_token = create_reset_token(user.email) # type: ignore
        db_logintoken=Login(refresh_token=refresh_token,expire_in=expire_in,email=user.email,token=token,login_at=datetime.utcnow())
        USER_LOGIN_DATA.append(user.email)
       
        db.add(db_logintoken)
        db.commit()
        db.refresh(db_logintoken)
        
        
        return {
            "id":db_logintoken.id if db_logintoken else None,
            "email":db_logintoken.email if db_logintoken else None,
            "access token":db_logintoken.token if db_logintoken else None,
            "refresh token":db_logintoken.refresh_token if db_logintoken else None,
           
           
    } 
        
    else:
        return None
    

###################################################################################################
#                                     CHANGE PASSWORD                                             #
###################################################################################################

   
def user_change_password(db: Session ,request: schemas.changepassword):
  
    
   
    user = db.query(AuthData).filter(AuthData.email == request.email).first()
    if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        
    if not verify_password(request.old_password, user.password):  # type: ignore
            raise HTTPException(status_code=400, detail="Invalid old password")
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password # type: ignore
    db.commit()
  
  
###################################################################################################
#                                     LOGOUT                                                      #
###################################################################################################
  
    
def logout_user(db: Session,logout_request: schemas.UserLogout ):   
    user_model = db.query(Login).filter(Login.email == logout_request.email).first()
    if user_model is None:
         return JSONResponse(status_code=404, content={"error":"User doesn't exists"})
    db.query(Login).filter(Login.email == logout_request.email).delete()
  

    db.commit()

###################################################################################################
#                                     FORGOT PASSWORD                                             #
###################################################################################################

def send_reset_password_email(db:Session,email: str):
    user = db.query(AuthData).filter(AuthData.email==email).first() # type: ignore
    if user:
        access_token=create_jwt_token({"sub":user.id})
        db_reset_token=PasswordAndAccessResetToken(email=email,access_token=access_token)
        db.add(db_reset_token)
        db.commit()
        db.refresh(db_reset_token)
        
        send_reset_email(email,access_token)
        
        return True
    return False


def user_reset_password(db: Session ,request:Request,reset_credentials: schemas.PasswordReset):
    user_data_id=request.headers.get('user_id')
    user_id=db.query(AuthData).filter_by(id=user_data_id).first()
    user = db.query(AuthData).filter_by(email=reset_credentials.email).first()
   
   
    if user:
       
        print("true")
        access_token = create_jwt_token({"sub":user.email})  # type: ignore
        db_resettoken=PasswordAndAccessResetToken(email=user.email,access_token=access_token)
        db.add(db_resettoken)
        hash_password=get_hashed_password(reset_credentials.new_password)
        user.password=hash_password # type: ignore
        db.commit()
        db.refresh(db_resettoken)
        
        return  {"message": "Password reset successfully"}
        
    else:
        return None
    

###################################################################################################
#                                     reset acceess token                                            #
###################################################################################################

def reset_acceess_token(db: Session ,data: schemas.ResetAccessTokenCreate):
    user=db.query(AuthData).filter(AuthData.email == data.email_access_token).first()
    token=db.query(AuthData).filter(AuthData.refresh_token == data.reset_refresh_token)
    
    if user or token:
        new_access_token=create_jwt_token({"sub":user.id}) # type: ignore
        db_reset_access_token=PasswordAndAccessResetToken(reset_access_token=new_access_token)
        db.add(db_reset_access_token)
        db.commit()
        db.refresh(db_reset_access_token)
        
        return f"access token:{db_reset_access_token.reset_access_token}"
        
        


   
  
  