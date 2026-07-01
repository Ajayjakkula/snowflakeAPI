from fastapi import FastAPI

from app.routes import router

app = FastAPI(

    title="Snowflake REST API",

    description="REST API to access Snowflake data",

    version="1.0",

    contact={

        "name": "Ajay",

        "email": "ajay@gmail.com"

    }

)

app.include_router(router)