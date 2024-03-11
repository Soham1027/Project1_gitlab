import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.models import AuthData,Tasks,SensorList
from auth import schemas


###################################################################################################
#                                      SERVICE GET LIST                                           #
###################################################################################################


def get_sensorlist(db: Session, sensorlist_id: int):
    return db.query(SensorList).filter(SensorList.id == sensorlist_id).first()


###################################################################################################
#                                      SERVICE GET ALL LISTS                                      #
###################################################################################################


def get_all_sensorlist(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SensorList).offset(skip).limit(limit).all()


###################################################################################################
#                                      SERVICE CREATE LIST                                        #
###################################################################################################


def create_new_sensorlist(db: Session,list: schemas.SensorListCreate):  
        db_list = SensorList(**list.dict())
        
        db.add(db_list)
        
        db.commit()
        db.commit()
        db.refresh(db_list)
        return db_list


###################################################################################################
#                                       SERVICE UPDATE LISTS                                      #
###################################################################################################


def update_sensorlist(db: Session, sensorlist_id: int, sensorlist: schemas.SensorListCreate):
    updated_rows=db.query(SensorList).filter(SensorList.id==sensorlist_id).update(sensorlist.dict(exclude_unset=True)) # type: ignore
    db.commit()
    if updated_rows >0 :
        updated_user=db.query(SensorList).filter(SensorList.id==sensorlist_id).first()
        return updated_user
    return None
    


###################################################################################################
#                                      SERVICE DELETE LISTS                                       #
###################################################################################################


def remove_sensorlist(db: Session):
    db.query(SensorList).delete()
    db.commit()
    

    