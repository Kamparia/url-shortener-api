import uvicorn
from fastapi import FastAPI
from api.router import router


# fastapi app
app = FastAPI(
    title="URL Shortener API",
    description="API for URL Shortener Microservice",
    version="0.1.0"
)

# add routers
app.include_router(router)


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')

# uvicorn main:app --reload
