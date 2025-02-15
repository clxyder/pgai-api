import factory
from faker import Faker
from faker.providers import misc

from app.common.models import User

fake = Faker()
fake.add_provider(misc)


class DbModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = "commit"

    # https://stackoverflow.com/a/76227997
    # https://github.com/FactoryBoy/factory_boy/issues/679
    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        instance = super()._create(model_class, *args, **kwargs)
        async with cls._meta.sqlalchemy_session as session:
            await session.commit()
            await session.refresh(instance)
        return instance


class UserFactory(DbModelFactory):
    class Meta:
        model = User

    name = factory.LazyFunction(lambda: fake.name())
    uuid = factory.LazyFunction(fake.uuid4)
