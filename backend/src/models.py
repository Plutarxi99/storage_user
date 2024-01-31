
from sqlalchemy import Boolean, Column, Integer, String

# from backend.src.database import Base
from src.database import Base


# модели для создания таблице в базе данных
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(45), nullable=True)
    last_name = Column(String(60), nullable=True)
    other_name = Column(String(45), nullable=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(13), nullable=True)
    birthday = Column(String, nullable=True)
    city = Column(String(60), nullable=True)
    additional_info = Column(String, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

