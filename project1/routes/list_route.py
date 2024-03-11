from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import schemas
from service import service_lists
from database import dependencies
from models import models
from utils.access_auth_baerer import AccessToken

router = APIRouter()




###################################################################################################
#                                      READ LIST                                                  #
###################################################################################################


@router.get("/sensors/{sensors_id}", response_model=schemas.SensorList,tags=['Sensors'])
def read_sensors(sensorlist_id:int,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    listdata=service_lists.get_sensorlist(db,sensorlist_id)
    if listdata is None:
       return JSONResponse(status_code=404, content={"error":"User doesn't exists"})
    return listdata


###################################################################################################
#                                      READ ALL LIST                                              #
###################################################################################################


@router.get("/sensors/", response_model=list[schemas.SensorList],tags=['Sensors'])
def read_all_sensors(skip:int=0,limit:int=100,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    sensorlists=service_lists.get_all_sensorlist(db,skip=skip,limit=limit)
    return sensorlists


###################################################################################################
#                                      CREATE LIST                                                #
###################################################################################################
 

@router.post("/sensors/", response_model=schemas.SensorList,tags=['Sensors'])
def create_list(sensorlists: schemas.SensorListCreate,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    return service_lists.create_new_sensorlist(db,sensorlists)


###################################################################################################
#                                      UPDATE LIST                                                #
###################################################################################################
 
    
@router.patch("/sensors/{sensors_id}",response_model=schemas.SensorList,tags=['Sensors'])
def update_sensors(sensorlist_id: int, sensorlist_update: schemas.SensorListBase, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
   
    return service_lists.update_sensorlist(db,sensorlist_id,sensorlist_update) # type: ignore

  
###################################################################################################
#                                       DELETE LIST                                               #
###################################################################################################
  
    
@router.delete("/sensors/",tags=['Sensors'])
def delete_sensorlist(sensorlist_id: int, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    sensorlist_model = db.query(models.SensorList).filter(
        models.SensorList.id == sensorlist_id).first()
    if sensorlist_model is None:
        return JSONResponse(status_code=404, content={"error":"Id doesn't exists"})
    db.query(models.SensorList).filter(
        models.SensorList.id == sensorlist_id).delete()

    db.commit()



   
