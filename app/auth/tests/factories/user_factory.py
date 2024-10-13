from factory import Faker

from auth.models import User

from common.factory import BaseFactory


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = Faker("email")
    hashed_password = "hashed_password"
    is_active = True
    first_name = Faker("first_name")
    last_name = Faker("last_name")
