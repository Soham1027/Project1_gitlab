from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import schemas
from service import service_tasksensor
from database import dependencies
from models import models
from utils.access_auth_baerer import AccessToken

router = APIRouter()




###################################################################################################
#                                      READ LIST                                                  #
###################################################################################################


@router.get("/tasksensor/{tasksensor_id}/", response_model=schemas.TaskSensor,tags=['Tasksensor'])
def read_data_tasksensorlist(tasksensor_id:int,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    listdata=service_tasksensor.get_tasksensorlist(db,tasksensor_id)
    if listdata is None:
        return JSONResponse(status_code=404, content={"error":"User doesn't exists"})
    return listdata



###################################################################################################
#                                      READ ALL LIST                                              #
###################################################################################################


@router.get("/tasksensor/", response_model=list[schemas.TaskSensor],tags=['Tasksensor'])
def read_tasksensorlist(skip:int=0,limit:int=100,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    lists=service_tasksensor.get_all_tasksensorlists(db,skip=skip,limit=limit)
    return lists


###################################################################################################
#                                      CREATE LIST                                                #
###################################################################################################
 

@router.post("/{list_id}/tasksensor/", response_model=schemas.TaskSensor,tags=['Tasksensor'])
def create_tasksensorlist(tasksensor_data: schemas.TaskSensorCreate,list_id:int,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    return service_tasksensor.create_new_tasksensorlist(db,list_id,tasksensor_data)



###################################################################################################
#                                      UPDATE LIST                                                #
###################################################################################################
 
    
@router.patch("/tasksensor/{tasksensor_id}",response_model=schemas.TaskSensor,tags=['Tasksensor'])
def update_tasksensorlist(tasksensor_id:int, list_update: schemas.TaskSensor, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
   
    return service_tasksensor.update_tasksensorlist(db,tasksensor_id,list_update) # type: ignore

  
###################################################################################################
#                                       DELETE LIST                                               #
###################################################################################################
  
    
@router.delete("/tasksensor/",tags=['Tasksensor'])
def delete_list(tasksensor_id: int, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    list_model = db.query(models.TaskSensor).filter(
        models.TaskSensor.id == tasksensor_id).first()
    if list_model is None:
          return JSONResponse(status_code=404, content={"error":"User doesn't exists"})
    db.query(models.TaskSensor).filter(
        models.TaskSensor.id == tasksensor_id).delete()

    db.commit()
