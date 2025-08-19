from sqlalchemy import Column, Integer, String
from .database import Base

# Define the User model
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, name={self.name}, age={self.age})>"