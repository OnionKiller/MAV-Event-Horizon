import hug
import api

from db import SqlAlchemyContext, DeclarativeBase, engine
from sqlalchemy.orm.session import Session


@hug.context_factory(apply_globally=True)
def create_context(*args, **kwargs):
    return SqlAlchemyContext()


@hug.delete_context()
def delete_context(
    context: SqlAlchemyContext,
    exception=None,
    errors=None,
    lacks_requirement=None,
):
    context.cleanup(exception)


@hug.directive()
def database(*args, context: SqlAlchemyContext = None, **kwargs):
    return context.db


@hug.extend_api()
def apis():
    return [api]


DeclarativeBase.metadata.create_all(bind=engine)
