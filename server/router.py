# FastAPI router module added seperately for easy access in python

from fastapi import FastAPI

# Router Declaration
router: FastAPI = FastAPI(docs_url='/api/docs', redoc_url='/api/redoc')