import uvicorn
from fastapi import FastAPI
from src.api.router import router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://185.27.192.116:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Methods",
    ],
)
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
