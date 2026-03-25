from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, cust, fact, item, user

app = FastAPI(title="TriSys API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth")
app.include_router(cust.router, prefix="/api/cust")
app.include_router(fact.router, prefix="/api/fact")
app.include_router(item.router, prefix="/api/item")
app.include_router(user.router, prefix="/api/user")
