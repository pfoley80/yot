from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from yot.models import initialize_sql
from yot.triggers import initialize_triggers

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    initialize_sql(engine)

    initialize_triggers(global_config, **settings)

    config = Configurator(settings=settings)
    config.add_static_view('static', 'yot:static')

    config.add_route('home', '/', view='yot.views.main',view_renderer='templates/human.pt')
    config.add_route('poll', '/poll/{recipient}', view='yot.views.client_poll', renderer="string")
    config.add_route('post', '/post', view='yot.views.client_post', renderer="json")
    config.add_route('add', '/add', view='yot.views.add_event', renderer="json")   

    return config.make_wsgi_app()


