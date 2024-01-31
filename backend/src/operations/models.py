from sqlalchemy import Boolean, Column, Integer, String

from backend.src.database import Base


# модели для создания таблице в базе данных
class User(Base):
    __tablename__ = 'users'

    # id = Column(Integer, primary_key=True)
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    other_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, nullable=True)
    birthday = Column(String, nullable=True)
    city = Column(String, nullable=True)
    additional_info = Column(String, nullable=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    # is_superuser = Column(Boolean, default=False)