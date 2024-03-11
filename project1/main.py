from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Annotated

from sqlalchemy.orm import Session
import uvicorn


from service import service_tasks, service_users,service_lists


from database.database import SessionLocal, engine
from database.dependencies import get_db
from models import models
from fastapi import FastAPI
from auth.middleware import MyMiddleware
import fastapi.openapi.utils as fu


app = FastAPI(title="BioProject")
fu.validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "error": {"title": "Message", "type": "string"}, 
    },
}

app.add_middleware(MyMiddleware)

from routes.user_route import router as user_router
from routes.authentication_route import router as authentication_router
from routes.task_route import router as task_router
from routes.list_route import router as list_router



app.include_router(user_router) 
app.include_router(authentication_router)

app.include_router(task_router)
app.include_router(list_router)


@app.on_event("startup")
async def startup_data_event():
    models.Base.metadata.create_all(bind=engine)
    print("database started")


@app.on_event("shutdown") 
async def shutdown_data_event():
    print("engine is Shutdown")
    
if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='192.168.130.41') # type: ignore