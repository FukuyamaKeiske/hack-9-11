import uvicorn
from . import app
from admin import app as flask_app
from fastapi.middleware.wsgi import WSGIMiddleware

@app.on_event("startup")
async def on_startup():
    print("FastAPI server is starting...")
    app.mount("/admin", WSGIMiddleware(flask_app))
    print("FastAPI server is started.")

def start():
    uvicorn.run(app, host="0.0.0.0", port=8000)
