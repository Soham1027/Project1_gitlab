import datetime
from sqlalchemy.orm import Session
from models.models import AuthData,Tasks
from auth import schemas
from utils.utils import get_hashed_password
from sqlalchemy import update




###################################################################################################
#                                      SERVICE GET USER                                           #
###################################################################################################


def get_user(db: Session, user_id: int):
    return db.query(AuthData).filter(AuthData.id == user_id).first()


###################################################################################################
#                                      SERVICE GET ALL USER                                       #
###################################################################################################


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(AuthData).offset(skip).limit(limit).all()




###################################################################################################
#                                      SERVICE UPDATE USER                                        #
###################################################################################################


def update_user(db: Session,user_id: int, user: schemas.UserBase):
    updated_rows=db.query(AuthData).filter(AuthData.id==user_id).update(user.dict(exclude_unset=True)) # type: ignore
    db.commit()
    if updated_rows >0 :
        updated_user=db.query(AuthData).filter(AuthData.id==user_id).first()
        return updated_user
    return None
###################################################################################################
#                                      SERVICE DELETE USER                                        #
###################################################################################################

   
def remove_user_messages(db:Session):
    db.query(AuthData).delete()
    db.commit()
    
    
