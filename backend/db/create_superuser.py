# from fastapi import Depends
# from sqlalchemy.orm import Session
#
# from backend.api.deps import get_db
# from backend.core.config import settings
# from backend.core.security import get_password_hash
# from backend.crud.users import get_user
# from backend.models import User

# TODO: доделать функцию для создание суперпользователя при создании базы данных
# def create_superuser(db: Session = Depends(get_db)):
# Tables should be created with Alembic migrations
# But if you don't want to use migrations, create
# the tables un-commenting the next line
# Base.metadata.create_all(bind=engine)
# user = get_user(db=db, email=settings.SUPERUSER_EMAIL)
# if not user:
#     db_obj = User(
#         email=settings.SUPERUSER_EMAIL,
#         password=get_password_hash(settings.SUPERUSER_PASSWORD),
#         is_admin=True,
#         is_active=True,
#         is_superuser=True
#     )
#     db.add(db_obj)
#     db.commit()
#     db.refresh(db_obj)
# pass
