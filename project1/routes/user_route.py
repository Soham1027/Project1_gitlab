from fastapi import APIRouter,Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from auth import schemas
from service import service_users

from database import dependencies
from models import models
from utils.access_auth_baerer import AccessToken


from utils.reset_auth_baerer import RefreshToken

router = APIRouter()




###################################################################################################
#                                     READ USER                                                   #
###################################################################################################


@router.get("/users/{user_id}", response_model=schemas.User,tags=['Users'])
def read_user(user_id:int,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    user=service_users.get_user(db,user_id)
    if user is None:
        return JSONResponse(status_code=404, content={"error":"Id doesn't exists"})
    return user


###################################################################################################
#                                      READ ALL USER                                              #
###################################################################################################


@router.get("/users/", response_model=list[schemas.User],tags=['Users'])
def read_users(skip:int=0,limit:int=100,db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    users=service_users.get_all_users(db,skip=skip,limit=limit)
    return users


###################################################################################################
#                                      UPDATE USER                                                #
###################################################################################################


@router.patch("/users/{user_id}",response_model=schemas.User,tags=['Users'])
def update_user(user_id: int, user_update: schemas.UserBase, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
   
    return service_users.update_user(db,user_id,user_update)


###################################################################################################
#                                      DELETE USER                                                #
###################################################################################################


@router.delete("/users/{user_id}",tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(dependencies.get_db),dependencies=Depends(AccessToken())):
    user_model = db.query(models.AuthData).filter(
        models.AuthData.id == user_id).first()
    if user_model is None:
         return JSONResponse(status_code=404, content={"error":"Id doesn't exists"})
    db.query(models.AuthData).filter(
        models.AuthData.id == user_id).delete()

    db.commit()



