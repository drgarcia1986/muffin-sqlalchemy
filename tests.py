import muffin
import pytest
from sqlalchemy import Column, Integer, String

from muffin_sqlalchemy import SqlAlchemyDeclarativeBase


class PersonModel(SqlAlchemyDeclarativeBase):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    def __init__(self, name):
        self.name = name


class PersonHandler(muffin.Handler):
    def get(self, request):
        name = request.match_info.get('name')
        session = request.sqlalchemy_session
        person = session.query(PersonModel).filter_by(name=name).first()
        return {'id': person.id, 'name': person.name}

    def post(self, request):
        data = yield from request.json()
        person = PersonModel(name=data['name'])
        session = request.sqlalchemy_session
        session.add(person)
        session.commit()
        return muffin.Response(status=201)


@pytest.fixture(scope='session')
def app(loop):
    return muffin.Application(
        'sqlalchemy_app', loop=loop,
        PLUGINS=('muffin_sqlalchemy',)
    )


def test_plugin_register(app):
    assert 'sqlalchemy' in app.ps
    assert 'database_uri' in app.ps.sqlalchemy.cfg


def test_create_database_command(app, capsys):
    with pytest.raises(SystemExit):
        app.manage(*'create_database'.split())

    out, err = capsys.readouterr()
    assert 'OK' in out


def test_middleware_add_session_in_request(app, client):

    @app.register('/session')
    def check_session(request):
        assert request.sqlalchemy_session
        return 'Ok'

    response = client.get('/session')
    assert response.text == 'Ok'


def test_use_sqlalchemy_session(app, client):
    app.register('/person', '/person/{name}')(PersonHandler)

    response = client.post_json('/person', {'name': 'foo'})
    assert response.status_code == 201

    response = client.get('/person/foo')
    assert response.status_code == 200
    assert response.json['name'] == 'foo'
