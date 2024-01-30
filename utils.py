# Utilities file
from database import db


# Clearing data from the state machine
async def clean_state(state) -> dict:
    async with state.proxy() as data:
        return data


# Adding data to the database
async def add_to_database(user_id: str, clean_data: dict, openai_response: str) -> None:
    # Create a SqlDB object
    database_sql = db.SqlDB()
    # Create the table if it does not exist
    database_sql.create_table()
    # Adding the cleansed data to the database
    database_sql.add_to_database(user_id=user_id, **clean_data, openai_response=openai_response)
    # Close sql connection
    database_sql.close_connection()
