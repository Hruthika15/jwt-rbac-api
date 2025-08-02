from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://postgres:12345@localhost:5433/postgres"

engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    SQLModel.metadata.create_all(engine)
