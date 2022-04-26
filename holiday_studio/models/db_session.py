import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.ext.declarative import DeclarativeMeta
import json


SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(connection_string):
    global __factory

    if __factory:
        return

    engine = sa.create_engine(connection_string, echo=True, connect_args={'check_same_thread': False})
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


# https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata' and x != "registry"]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)