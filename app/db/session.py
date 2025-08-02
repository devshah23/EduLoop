from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()  

DATABASE_URL: str = os.getenv("DATABASE_URL","")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables.")

engine = create_async_engine(DATABASE_URL, future=True)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
