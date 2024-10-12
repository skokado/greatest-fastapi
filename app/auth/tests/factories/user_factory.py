from factory.alchemy import SQLAlchemyModelFactory
from factory import Faker

from common.dependencies.db import SessionLocal

from ...models import User

fake = Faker("ja")


class UserFactory(SQLAlchemyModelFactory):

    class Meta:
        model = User
        sqlalchemy_session_factory = lambda: SessionLocal()
        sqlalchemy_session_persistence = "commit"

    email = Faker("email")
    hashed_password = "hashed_password"
    is_active = True
    first_name = Faker("first_name")
    last_name = Faker("last_name")
