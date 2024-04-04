from sqlalchemy import Column, String, Integer, Boolean

from AbstractModel import AbstractModel


class User(AbstractModel):
    __tablename__ = "users"

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True, index=True)
    code = Column(Integer, default=None)
    role = Column(String)
    photo = Column(String, nullable=True)
    #phone = Column(String, nullable=False, unique=True, index=True)
    #phone_confirmed = Column(Boolean, default=False)
    email_confirmed = Column(Boolean, default=False)