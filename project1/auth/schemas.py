from enum import Enum
import re
from email_validator import EmailNotValidError
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field,EmailStr, validate_email,validator
from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import date, datetime
from models import models
 
###################################################################################################
#                                      USER  SCHEMAS                                              #
###################################################################################################


    

class UserBase(BaseModel):
    name: str
    email:EmailStr 
    role:str
   
    @validator("email")
    def email_validator(cls, email):
        regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")  
        if re.fullmatch(regex,email):
            if(str(email).split('@')[1].split(".")[0])=="example":
               raise HTTPException(status_code=400 ,detail="please give valid domain") 
            else:  
                return email
          
        else:
          raise HTTPException(status_code=400,detail="Invalid Email")

class UserCreate(UserBase):
    password: str

    @validator("password")
    def password_validator(cls, password):
        if len(password) < 8:
            raise HTTPException(status_code=400,detail= "password must be at least 8 characters long")
        return password
        



class User(UserBase):
    id:int
   
    
 
    class Config:
      from_attributes = True

   
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordReset(BaseModel):
    email:str
    new_password:str
  

class UserLogout(BaseModel):
    email: str
    
        
class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token:str


class TokenData(BaseModel):
    email: str 

  
class changepassword(BaseModel):
    email:str
    old_password:str
    new_password:str

    
###################################################################################################
#                                      Tasksensor SCHEMAS                                               #
###################################################################################################
class TaskSensorBase(BaseModel):
     task_id:int
    # task_data_id: int


class TaskSensorCreate(TaskSensorBase):
    pass
 


class TaskSensor(TaskSensorBase):
    list_id: int

   
    class Config:
      from_attributes = True
      
 ###################################################################################################
#                                      LIST SCHEMAS                                               #
###################################################################################################     


class SensorListBase(BaseModel):
  
    name:str
    is_clicked: bool = True
    started_at:date
    end_at:date
   
  
    @validator('started_at', pre=True)
    def parse_started_at(cls, value):
        return datetime.strptime(value, '%Y-%m-%d')
    
    @validator('end_at', pre=True)
    def parse_end_at(cls, value):
        return datetime.strptime(value, '%Y-%m-%d')
    # task_data_id: int
    

class SensorListCreate(SensorListBase):
    pass


class SensorList(SensorListBase):
    id:int
  

    class Config:
      from_attributes = True
      

      
      
      
###################################################################################################
#                                      TASK SCHEMAS                                               #
###################################################################################################
      
 
class TaskBase(BaseModel):
   
    name: str = Field(max_length=50)
    
    started_at:date
    end_at:date
    sensors: List[int] 
  
  
    
    @validator('end_at', pre=True) 
    def parse_end_at(cls,end_date):
      
        return datetime.strptime(end_date, '%Y-%m-%d')
    
    
   
    
    

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id:int
   
  
    # lists: List[DataList]
   
    
   
  
    class Config:
        from_attributes = True
        

###################################################################################################
#                                      EXPRIMENTS SCHEMAS                                         #
###################################################################################################

class ExperimentBase(BaseModel):
    name: str = Field(max_length=50)
    group:str
    started_by:str
    organism:str
    medium:str
    inocolumn:str
    created_at:datetime
    ended_at:str
    
class ExperimentCreate(ExperimentBase):
    pass

class Experiment(ExperimentBase):
    id: int
  
   
    class Config:
        from_attributes = True
        
        


###################################################################################################
#                                      RESET ACCESS SCHEMAS                                       #
###################################################################################################
class ResetAccessTokenBase(BaseModel):
    email_access_token:Optional[str] =None
    reset_refresh_token:Optional[str] =None

    @validator("email_access_token")
    def email_validator(cls, email_access_token):
        if ((email_access_token).split("@")[-1].split(".")[0])=="gmail" :
           
            return email_access_token
        else:
          raise ValueError('please give valid format EX.abc@gmail.com')

    
class ResetAccessTokenCreate(ResetAccessTokenBase):
    pass

class ResetAccessToken(ResetAccessTokenBase):
    id: int
  
   
    class Config:
        from_attributes = True
        
        








