import uvicorn
from fastapi import FastAPI

from routers.id_detection_router import id_router

app = FastAPI()
app.include_router(id_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)