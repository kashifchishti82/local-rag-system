from .database import engine, Base, get_db
from .models import User

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
