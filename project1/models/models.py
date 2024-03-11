import datetime
from typing import List
from sqlalchemy import Column, ForeignKey,Integer,String,Boolean,DateTime,Float,ARRAY
from database.database import Base
from sqlalchemy.orm import relationship,deferred
from sqlalchemy.sql import func




class AuthData(Base):
    __tablename__="datas"
    
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String(50),unique=True) # type: ignore
    name=Column(String(50),unique=True)
    role=Column(String)
    password=Column(String)
    token=Column(String, nullable=True)
    refresh_token=Column(String,nullable=True)
    expire_in=Column(String)
    created_at= Column(DateTime(timezone=True), server_default=func.now())
    updated_at=Column(DateTime)



class Login(Base):
    __tablename__="login"
    
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String)
    token=Column(String)
    refresh_token=Column(String)
    expire_in=Column(String)
    login_at= Column(DateTime(timezone=True), server_default=func.now())


class PasswordAndAccessResetToken(Base):
    __tablename__="reset_password_access_token"
    
    id=Column(Integer,primary_key=True,index=True) 
    email=Column(String)
    access_token=Column(String)
    email_access_token=Column(String)
    reset_refresh_token=Column(String)
    reset_access_token=Column(String)

    
class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now())
    started_at = Column(String)
    end_at = Column(String)
    name = Column(String, unique=True)
    user_id=Column(Integer)
    sensorlist = relationship("TaskSensor", back_populates="tasksensor_taskdatas")
    


class SensorList(Base):
    __tablename__ = "sensors"
    
    id = Column(Integer, primary_key=True, index=True)
    name=Column(String(50),unique=True)
    is_clicked = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),server_default=func.now())
    started_at = Column(String)
    end_at = Column(String)
    listdatas = relationship("TaskSensor", back_populates="tasksensor_listdatas")

  
class TaskSensor(Base):
    __tablename__ = "task_sensor"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id=Column(Integer,ForeignKey("tasks.id",ondelete='CASCADE'))
    tasksensor_taskdatas = relationship("Tasks", back_populates="sensorlist",passive_deletes=True)
    list_id=Column(Integer,ForeignKey("sensors.id"))
    tasksensor_listdatas = relationship("SensorList", back_populates="listdatas")
      

    
