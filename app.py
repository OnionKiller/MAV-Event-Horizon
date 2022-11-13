import hug
import api

from db import SqlAlchemyContext,DeclarativeBase,engine
from sqlalchemy.orm.session import Session


@hug.context_factory()
def create_context(*args,**kwargs):
    return SqlAlchemyContext()

@hug.delete_context()
def delete_context(context: SqlAlchemyContext, exception=None, errors=None, lacks_requirement=None):
    context.cleanup(exception)

@hug.directive()
class SqlalchemySession(Session):
    def __new__(cls, *args, context: SqlAlchemyContext = None, **kwargs):
        return context.db

@hug.extend_api()
def apis():
    return [api]

DeclarativeBase.metadata.create_all(bind=engine)