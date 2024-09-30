from sqlalchemy.ext.asyncio import create_async_engine
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection details from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", "5432")  # Default PostgreSQL port

# Create an async SQLAlchemy engine
engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}")

async def test_connection():
    try:
        async with engine.connect() as connection:
            print("Successfully connected to the database!")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")

# Run the test
asyncio.run(test_connection())