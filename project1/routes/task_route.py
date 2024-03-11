from typing import Annotated, List,Optional
from fastapi import APIRouter,Depends, HTTPException, Header, Response,Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from auth import schemas
from service import service_tasks
from database import dependencies
from models import models
from fastapi.encoders import jsonable_encoder
from utils.access_auth_baerer import AccessToken

router = APIRouter()




###################################################################################################
#                                       TASK WITH SENSORS                                               #
###################################################################################################


           

@router.get("/task/{task_id}",tags=['Tasks'])
def get_tasks_by_task_id(request:Request,task_id:int,db:Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    db_data = service_tasks.get_data_user(db,request,task_id)
    
    return(db_data)

   
   

###################################################################################################
#                                      READ ALL TASKS                                             #
###################################################################################################
   

@router.get("/tasks/",tags=['Tasks'])
def read_all_tasks(request:Request,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    tasks=service_tasks.get_all_tasks(db,request)
    return(jsonable_encoder(tasks))


###################################################################################################
#                                      CREATE TASK                                                #
###################################################################################################
   

@router.post("/tasks/", response_model=dict,tags=['Tasks'])
def create_task(tasks: schemas.TaskCreate,request:Request,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    
    create_task_data= service_tasks.create_new_task(db,request,tasks) 
    return(create_task_data)

    
###################################################################################################
#                                      UPDATE TASK                                                #
###################################################################################################


@router.patch("/tasks/{task_id}",response_model=schemas.Task,tags=['Tasks'])
def update_task_data(task: schemas.TaskBase,task_id:int, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
   
    return service_tasks.update_task(db,task_id,task) # type: ignore


###################################################################################################
#                                      DELETE TASK                                                #
###################################################################################################

   
@router.delete("/tasks/{task_id}",tags=['Tasks'])
def delete_task(task_id: int, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    task_model = db.query(models.Tasks).filter(
        models.Tasks.id == task_id).first()
    if task_model is None:
           return JSONResponse(status_code=404, content={"error":"Id doesn't exists"})
    db.query(models.Tasks).filter(
        models.Tasks.id == task_id).delete()

    db.commit()



