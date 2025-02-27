import factory
from factory.alchemy import SESSION_PERSISTENCE_COMMIT, SESSION_PERSISTENCE_FLUSH
from faker import Faker
from faker.providers import misc

from app.common.models import Page, User

fake = Faker()
fake.add_provider(misc)


class DbModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True
        sqlalchemy_session_persistence = SESSION_PERSISTENCE_COMMIT

    # https://stackoverflow.com/a/76227997
    # https://github.com/FactoryBoy/factory_boy/issues/679
    @classmethod
    async def _save(cls, model_class, session, args, kwargs):
        session_persistence = cls._meta.sqlalchemy_session_persistence

        obj = model_class(*args, **kwargs)
        session.add(obj)
        if session_persistence == SESSION_PERSISTENCE_FLUSH:
            await session.flush()
        elif session_persistence == SESSION_PERSISTENCE_COMMIT:
            await session.commit()
        await session.refresh(obj)
        return obj


class UserFactory(DbModelFactory):
    class Meta:
        model = User

    name = factory.LazyFunction(lambda: fake.name())
    uuid = factory.LazyFunction(fake.uuid4)


class PageFactory(DbModelFactory):
    class Meta:
        model = Page

    title = factory.LazyFunction(lambda: fake.sentence())
    content = factory.LazyFunction(lambda: "".join(fake.paragraphs()))
