# Combination of GraphQL and Fastapi

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import strawberry
from sqlalchemy.orm import Session

from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

# =============================================================================================================

DATABASE_URL = "mysql+pymysql://root:1234@192.168.11.30:3308/padafand"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

# =============================================================================================================

@strawberry.type
class UserType:
    id: int
    username: str
    hashed_password: str
    is_active: bool

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> UserType:
        db: Session = SessionLocal()
        user = db.query(User).filter(User.id == id).first()
        return UserType(id=user.id, username=user.username, hashed_password=user.hashed_password, is_active=user.is_active)

    @strawberry.field
    def all_users(self) -> list[UserType]:
        db: Session = SessionLocal()
        users = db.query(User).all()
        return [UserType(id=user.id, username=user.username, hashed_password=user.hashed_password, is_active=user.is_active) for user in users]

schema = strawberry.Schema(query=Query)

# =============================================================================================================

app = FastAPI()

graphql_app = GraphQLRouter(schema=schema)
app.include_router(graphql_app, prefix="/graphql")

# =============================================================================================================
