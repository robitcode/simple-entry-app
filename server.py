from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse # NOTE: NECESSARY FOR File responses!!!
from pydantic import BaseModel
from typing import Optional

# Declare Pydantic Model
class Input(BaseModel):
    name:str
    surname:Optional[str]
    address:str

# Create db 
from db import engine, SessionLocal, Entry
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# Helper Function 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def home():
    path = "form.html"
    return FileResponse(path) # Send the html file over

@app.get("/all")
def get_all(db:Session = Depends(get_db)):
    all_entries = db.query(Entry).all()
    return {"entries":all_entries}

@app.post("/select")
def search_db(entry:Input,db:Session = Depends(get_db)):
    search = db.query(Entry).filter(Entry.name == entry.name).first()
    if(search):
        return {"message":"Found the given item","entry":search}
    else:
        return {"error":"No Entries found."}

@app.post("/create")
def create_db(entry:Input,db:Session = Depends(get_db)):
    # Check if entry already exists
    check = db.query(Entry).filter(
        Entry.name == entry.name,
        Entry.surname == entry.surname,
        Entry.address == entry.address
        ).first()
    if(check):
        return {"error":"Entry already exists"}
    else:
        newentry = Entry(name = entry.name,surname = entry.surname, address = entry.address)
        db.add(newentry)
        db.commit()
        db.refresh(newentry)
        return {"message":"Sucessfully added entry","id":newentry.id}
    
@app.post("/delete")
def delete_db(entry:Input,db:Session = Depends(get_db)):
    deleted = db.query(Entry).filter(Entry.name == entry.name, Entry.surname == entry.surname).first()
    if(deleted):
        db.delete(deleted)
        db.commit()
        return {"message":"Sucessfully deleted entry","id":deleted.id}
    else:
        return{"error":"Entry not found"}