from fastapi import FastAPI, Depends, HTTPException
from app.schemas import CustomerCreate, CustomerOut, UserRead, UserCreate, UserUpdate
from uuid import UUID
from app.db import Customer, get_db, init_db
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.users import current_active_user, fastapi_users, User, auth_backend
from fastapi.responses import HTMLResponse
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

# allow requests from the frontend regardless of origin (for development purposes)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "null",  # for opening index.html directly from file system
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html for root path (MUST be before mount)
@app.get("/", response_class=HTMLResponse)
async def root():
    with open(Path(__file__).parent / "static" / "index.html", "r") as f:
        return f.read()

#Include all API routes BEFORE mounting static files
app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])
app.include_router(fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])


# @app.get("/health")
# def health_check():
#     return {"status": "healthy and working fine!"}

@app.post("/customers", response_model=CustomerOut)
async def create_customer(name: str, phone: str = None, address: str = None, notes: str = None, session: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    customer = Customer(name=name, phone=phone, address=address, notes=notes, user_id=user.id if user else None)
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[CustomerOut])
async def list_customers(session: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    result = await session.execute(select(Customer).where(Customer.user_id == user.id).order_by(Customer.created_at.desc()))
    customers = result.scalars().all()
    return customers

@app.get("/customers/{customer_id}", response_model=CustomerOut) 
async def get_customer(customer_id: UUID, session: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    result = await session.execute(select(Customer).where(Customer.id == customer_id, Customer.user_id == user.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: UUID, session: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    result = await session.execute(select(Customer).where(Customer.id == customer_id, Customer.user_id == user.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    await session.delete(customer)
    await session.commit()
    return {"detail": "Customer deleted successfully"}

@app.put("/customers/{customer_id}", response_model=CustomerOut)
async def update_customer(customer_id: UUID, name: str = None, phone: str = None, address: str = None, notes: str = None, session: AsyncSession = Depends(get_db), user: User = Depends(current_active_user)):
    result = await session.execute(select(Customer).where(Customer.id == customer_id, Customer.user_id == user.id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if name is not None:
        customer.name = name
    if phone is not None:
        customer.phone = phone
    if address is not None:
        customer.address = address
    if notes is not None:
        customer.notes = notes
    
    await session.commit()
    await session.refresh(customer)
    return customer


from fastapi.staticfiles import StaticFiles

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
