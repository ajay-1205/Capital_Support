from collections.abc import AsyncGenerator
import uuid
from sqlalchemy import UUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends

# Use SQLite with aiosqlite (simple, works on Render free tier)
DATABASE_URL = "sqlite+aiosqlite:///./capital_support.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    customers = relationship("Customer", back_populates="user")

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    # email = Column(String, unique=True, index=True, nullable=False)
    # hashed_password = Column(String, nullable=False)
    # is_active = Column(bool, default=True)
    # is_superuser = Column(bool, default=False)
    # is_verified = Column(bool, default=False)






class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="customers")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)
