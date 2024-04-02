from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId

app = FastAPI()

origins = [
    "http://localhost:3000",  # React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str
    password: str
    confirmPassword: str
    email: str
    phoneNumber: str

# Connect to MongoDB
client = AsyncIOMotorClient('mongodb://localhost:27017')
db = client['mydatabase']
collection = db['users']

@app.post("/register/")
async def register(user: User):
    print(f"Received data: {user.dict()}")  # Print received data

    # Check for unique username and email
    existing_user = await collection.find_one({"username": user.username})
    if existing_user:
        detail = "Username is already taken."
        print(detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        detail = "Email is already registered."
        print(detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    existing_user = await collection.find_one({"phoneNumber": user.phoneNumber})
    if existing_user:
        detail = "Phone number is already registered."
        print(detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    # Save the new user
    new_user = user.dict()
    new_user["_id"] = str(ObjectId())  # Generate a unique ID for the user
    await collection.insert_one(new_user)

    return {"message": "User registered successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)