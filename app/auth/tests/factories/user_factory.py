import factory
from factory import Faker
import factory.fuzzy

from auth.models import User

from auth.utils.password import hash_password
from common.factory import BaseFactory


def generate_password() -> str:
    return hash_password("password")


class UserFactory(BaseFactory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n)
    email = Faker("email")
    hashed_password = factory.fuzzy.FuzzyAttribute(generate_password)
    is_active = True
    first_name = Faker("first_name")
    last_name = Faker("last_name")
