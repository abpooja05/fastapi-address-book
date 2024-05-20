from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, condecimal
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from databases import Database
from geopy.distance import geodesic

# Database URL for SQLite
DATABASE_URL = "sqlite:///./test.db"

# Create a Database instance
database = Database(DATABASE_URL)
# Create a SQLAlchemy engine
engine = create_engine(DATABASE_URL)
# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a base class for the models
Base = declarative_base()

# SQLAlchemy model for the Address table
class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

# Pydantic model for input validation
class AddressCreate(BaseModel):
    name: str
    latitude: condecimal(max_digits=8, decimal_places=6) = Field(..., ge=-90.0, le=90.0)
    longitude: condecimal(max_digits=9, decimal_places=6) = Field(..., ge=-180.0, le=180.0)

# Initialize the FastAPI app
app = FastAPI()

# Event handler to connect to the database at startup
@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(bind=engine)

# Event handler to disconnect from the database at shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new address
@app.post("/addresses/", response_model=AddressCreate)
async def create_address(address: AddressCreate, db: Session = Depends(get_db)):
    db_address = Address(name=address.name, latitude=address.latitude, longitude=address.longitude)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

# Endpoint to retrieve an address by ID
@app.get("/addresses/{address_id}", response_model=AddressCreate)
async def read_address(address_id: int, db: Session = Depends(get_db)):
    address = db.query(Address).filter(Address.id == address_id).first()
    if address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

# Endpoint to update an address by ID
@app.put("/addresses/{address_id}", response_model=AddressCreate)
async def update_address(address_id: int, address: AddressCreate, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db_address.name = address.name
    db_address.latitude = address.latitude
    db_address.longitude = address.longitude
    db.commit()
    db.refresh(db_address)
    return db_address

# Endpoint to delete an address by ID
@app.delete("/addresses/{address_id}", response_model=AddressCreate)
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if db_address is None:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return db_address

# Endpoint to retrieve addresses within a given distance from specified coordinates
@app.get("/addresses/")
async def read_addresses_within_distance(lat: float, lon: float, distance: float, db: Session = Depends(get_db)):
    addresses = db.query(Address).all()
    result = []
    for address in addresses:
        if geodesic((lat, lon), (address.latitude, address.longitude)).km <= distance:
            result.append(address)
    return result

# Entry point to run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
