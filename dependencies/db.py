# Application
from database.db import session  # Session


# Get DB
def get_db():
    db = session()

    try:
        yield db
    finally:
        db.close()
