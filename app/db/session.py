from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import QueuePool
import os

DATABASE_URL = os.getenv("DATABASE_URL","")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables.")

engine = create_async_engine(
    DATABASE_URL,
    future=True,
    connect_args={"ssl": "require"},
    poolclass=QueuePool,           
    pool_size=10,
    max_overflow=5,
    pool_recycle=300,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
