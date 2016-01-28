""" Support SqlAlchemy in Muffin framework. """
import asyncio

from muffin.plugins import BasePlugin

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


__version__ = "0.0.3"
__project__ = "muffin-sqlalchemy"
__author__ = "Diego Garcia <drgarcia1986@gmail.com>"
__license__ = "MIT"


SqlAlchemyDeclarativeBase = declarative_base()


class Plugin(BasePlugin):

    """ SqlAlchemy Plugin. """

    name = 'sqlalchemy'
    defaults = {
        'database_uri': 'sqlite:///muffin.db',
    }

    def __init__(self, *args, **kwargs):
        """ Initialize the Plugin. """
        super().__init__(*args, **kwargs)

    def setup(self, app):
        """ Setup self. """
        super().setup(app)

        self.sqlalchemy_engine = create_engine(self.cfg.database_uri)
        self.session_builder = sessionmaker(bind=self.sqlalchemy_engine)

        @app.manage.command
        def create_database():
            SqlAlchemyDeclarativeBase.metadata.create_all(
                self.sqlalchemy_engine
            )
            print('OK')

    @asyncio.coroutine
    def sqlalchemy_middleware(self, app, handler):
        """Set session from request."""

        @asyncio.coroutine
        def middleware(request):
            request.sqlalchemy_session = self.session_builder()
            return (yield from handler(request))

        return middleware

    def start(self, app):
        """ Start plugin. """
        app.middlewares.insert(0, self.sqlalchemy_middleware)

    def finish(self, app):
        """ Finish plugin. """
        pass
