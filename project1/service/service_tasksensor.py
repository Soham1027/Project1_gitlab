
from sqlalchemy.orm import Session
from models.models import TaskSensor
from auth import schemas


###################################################################################################
#                                      SERVICE GET LIST                                           #
###################################################################################################


def get_tasksensorlist(db: Session, tasksensor_id: int):
    return db.query(TaskSensor).filter(TaskSensor.id == tasksensor_id).first()


###################################################################################################
#                                      SERVICE GET ALL LISTS                                      #
###################################################################################################


def get_all_tasksensorlists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskSensor).offset(skip).limit(limit).all()


###################################################################################################
#                                      SERVICE CREATE LIST                                        #
###################################################################################################


def create_new_tasksensorlist(db: Session,list_id:int, tasksensor_data: schemas.TaskSensorCreate):
    
        
        db_list = TaskSensor(**tasksensor_data.dict(),list_id=list_id)
        db.add(db_list)
        db.commit()
        db.refresh(db_list)
        return db_list
    
             
   

###################################################################################################
#                                       SERVICE UPDATE LISTS                                      #
###################################################################################################


def update_tasksensorlist(db: Session, tasksensor_id: int, list: schemas.TaskSensor):
    updated_rows=db.query(TaskSensor).filter(TaskSensor.id==tasksensor_id).update(list.dict(exclude_unset=True)) # type: ignore
    db.commit()
    if updated_rows >0 :
        updated_user=db.query(TaskSensor).filter(TaskSensor.id==tasksensor_id).first()
        return updated_user
    return None
   

###################################################################################################
#                                      SERVICE DELETE LISTS                                       #
###################################################################################################


def remove_all_tasksensorlists(db: Session):
    db.query(TaskSensor).delete()
    db.commit()