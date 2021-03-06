from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from .security import EntryFactory
import os

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    if 'DATABASE_URL' in os.environ:
        settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    secret = os.environ.get('AUTH_SECRET', 'somesecret')
    config = Configurator(
        settings=settings,
        authentication_policy=AuthTktAuthenticationPolicy(secret),    # the somesecret is the key to the castle
        authorization_policy=ACLAuthorizationPolicy(),
        default_permission='view'
        )
    config.include('pyramid_jinja2')    # changed from 'pyramid_chameleon'
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', factory=EntryFactory)    # the route order makes a difference. Go from more detail to less
    config.add_route('detail', '/journal/{id:\d+}', factory=EntryFactory)
    config.add_route('action', '/journal/{action}', factory=EntryFactory)
    config.add_route('auth', '/sign/{action}', factory=EntryFactory)
    config.scan()
    return config.make_wsgi_app()
