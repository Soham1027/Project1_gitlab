
import json
from typing import Annotated, Optional
from fastapi import HTTPException, Header, Request,Response
from fastapi.responses import JSONResponse
from sqlalchemy import select, text
from sqlalchemy.orm import Session,joinedload
from models.models import AuthData,Tasks,SensorList,TaskSensor
from auth import schemas
from service.service_tasksensor import create_new_tasksensorlist
from fastapi.encoders import jsonable_encoder



###################################################################################################
#                                      SERVICE GET ALL TASK                                       #
###################################################################################################


def get_all_tasks(db: Session,request:Request):
    
   
    user_data_id=request.headers.get('user_id')
    task_all_data=db.query(Tasks).filter(Tasks.user_id==user_data_id)
   
   
    main_data_list=[]
   
    
    
   
         
    for task in task_all_data:
        
        
        user_listdata= db.query(SensorList).join(TaskSensor,SensorList.id==TaskSensor.list_id).filter(TaskSensor.task_id==task.id).all()
        sensors_list=[{"id":j.id,"name":j.name} for j in user_listdata]

    
  
        tasks_datas={"id":task.id,"name":task.name,"started_at":task.started_at,"end_at":task.end_at,"sensors":sensors_list}
        main_data_list.append(tasks_datas)
    print("dataddas",(main_data_list))
    return(main_data_list)
    
    
 


###################################################################################################
#                                      SERVICE GET TASK                                           #
###################################################################################################




###################################################################################################
#                                      SERVICE CREATE TASK                                        #
###################################################################################################


def create_new_task(db: Session,request:Request,task: schemas.TaskCreate):
   
    
    user_data_id=request.headers.get('user_id')
    db_task = Tasks(name=task.name,started_at=task.started_at,end_at=task.end_at,user_id=user_data_id)
   
    db.add(db_task)
    db.commit()
   
    data_db_task_sensor=[]
    for ids in task.sensors:
       
        
        db_task_sensor=TaskSensor(task_id=db_task.id,list_id=ids)
        data_db_task_sensor.append((jsonable_encoder(db_task_sensor)))
        db.add(db_task_sensor)
        db.commit()
        db.refresh(db_task_sensor)
     
    
    db.refresh(db_task)
   
    response_data={"db_task":jsonable_encoder(db_task),"db_sensor":jsonable_encoder(data_db_task_sensor)}
   
    return(response_data)
    

                            



###################################################################################################
#                                      SERVICE UPDATE TASK                                        #
###################################################################################################


def update_task(db: Session,task_id:int, task: schemas.TaskBase):
  
  
    db_task = db.query(Tasks).filter(Tasks.id == task_id).first()
    
    if db_task:
        for key, value in task.dict(exclude_unset=True).items():
            setattr(db_task, key, value)
        
       
        db.query(TaskSensor).filter(TaskSensor.task_id == task_id).delete()
        for sensor_id in task.sensors:
            db_task_sensor = TaskSensor(task_id=task_id, list_id=sensor_id)
            db.add(db_task_sensor)
        
        db.commit()
        db.refresh(db_task)
        
    return db_task
 

###################################################################################################
#                                      SERVICE DELETE TASK                                        #
###################################################################################################


def remove_task(db: Session):
    db.query(Tasks).delete()
    db.commit()


###################################################################################################
#                                      SERVICE GET TASK WITH SENSOR                                       #
###################################################################################################



def get_data_user(db: Session,request:Request,task_id:int):
    user_data_id=request.headers.get('user_id') 
   
    ##########main###################
    user_taskdata= db.query(Tasks).filter(Tasks.user_id==user_data_id).filter(Tasks.id==task_id).first()
    user_listdata= db.query(SensorList).join(TaskSensor,SensorList.id==TaskSensor.list_id).filter(TaskSensor.task_id==task_id).all()
    sensor_lists=[]
    task_lists=[] 
    if user_taskdata:
   
        for user_data in user_listdata:
            sensor_lists.append({"id":user_data.id,"name":user_data.name})
        
    
        return({
                "id":user_taskdata.id if user_taskdata else None,
                "name":user_taskdata.name if user_taskdata else None,
                "started_at":user_taskdata.started_at if user_taskdata else None,
                "end_at":user_taskdata.end_at if user_taskdata else None,
                "sensors":sensor_lists
            
            
            
        })
    else:
        return JSONResponse(status_code=400,content={"message":"user didnt create this task"})
          


    
        


    
        

      
    
        
