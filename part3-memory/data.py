import os
import asyncio
import chainlit.data as cl_data
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database, database_exists

# Get database connection details from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME", "companion")


def create_data_layer():

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Create the database if it doesn't exist
    if create_database_if_not_exists():
        # Run the schema creation after ensuring the database exists
        asyncio.run(create_schema())

    # Create the data layer
    cl_data._data_layer = SQLAlchemyDataLayer(conninfo=DATABASE_URL)

# Function to create the database if it doesn't exist
def create_database_if_not_exists()->bool:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        # Check if the database exists
        if not database_exists(DATABASE_URL):
            # If not, create the database
            create_database(DATABASE_URL)
            print(f"Database '{DB_NAME}' created successfully!")
            return True
        else:
            print(f"Database '{DB_NAME}' already exists.")
            return False
    except Exception as e:
        print(f"Error creating or checking the database: {e}")
        return False

# Function to create the schema using async SQLAlchemy engine
async def create_schema():
    # Path to the SQL script that creates the database and schema
    sql_file_path = os.path.join("resources", "database.sql")

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    try:
        # Create an async SQLAlchemy engine connected to the 'companion' database
        engine = create_async_engine(DATABASE_URL, isolation_level='AUTOCOMMIT',)
        async with engine.connect() as connection:
            # Read and execute the SQL schema creation script
            with open(sql_file_path, 'r') as file:
                create_schema_sql = file.read()

            # Clean up the SQL statements by joining multi-line statements into a single line
            cleaned_statements = ' '.join(line.strip() for line in create_schema_sql.splitlines())

            # Split the cleaned SQL by semicolons
            statements = cleaned_statements.split(';')

            for statement in statements:
                if statement.strip():
                    await connection.execute(text(statement.strip()))
        print("Schema setup completed successfully!")
    except Exception as e:
        print(f"Error creating schema: {e}")


# Main execution block
if __name__ == "__main__":
    # Create the database if it doesn't exist
    if create_database_if_not_exists():
        # Run the schema creation after ensuring the database exists
        asyncio.run(create_schema())
