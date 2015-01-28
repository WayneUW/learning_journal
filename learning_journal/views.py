# from pyramid.response import Response    # commented out for Session2 homework
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPFound    # hmmm... added this for Using the matchdict
# from pyramid.exceptions import HTTPNotFound
# from pyramid.exceptions import HTTPFound
# from .forms import EntryCreateForm    # commented out for Session2 homework

# from sqlalchemy.exc import DBAPIError    # commented out for Session2 homework

from pyramid.security import forget, remember, authenticated_userid
from pyramid.view import view_config

from .models import (
    DBSession,
    MyModel,
    Entry,
    User
    )


from .forms import (    # added for Session2 homework
    EntryCreateForm,    # added for Session2 homework
    EntryEditForm,    # added for Session2 homework
    LoginForm   
)

import logging
logger = logging.getLogger("views.py")
# @view_config(route_name='home', renderer='templates/mytemplate.pt')
# def my_view(request):
#     try:
#         one = DBSession.query(MyModel).filter(MyModel.name == 'one').first()
#     except DBAPIError:
#         return Response(conn_err_msg, content_type='text/plain', status_int=500)
#     return {'one': one, 'project': 'learning_journal'}
# @view_config(route_name='auth', match_param='action=out', renderer='string')

@view_config(route_name='auth', match_param='action=in', renderer='string',
            request_method='POST')

def sign_in(request):
    login_form = None
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
    if login_form and login_form.validate():
        user = User.by_name(login_form.username.data)
        if user and user.verify_password(login_form.password.data):
            headers = remember(request, user.name)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('home'), headers=headers)


# @view_config( route_name='home', renderer='string' )   # original swapped for 3rd edit. String is the default renderer
@view_config(route_name='home', renderer='templates/list.jinja2')    # 3rd edit
def index_page(request):    # no change
    entries = []#Entry.all()    # 2nd edit
    print DBSession.bind
    form = None
    if not authenticated_userid(request):
        form = LoginForm()
        # return 'list page'    # 1st edit
    return {'entries': entries, 'login_form': form}    # 2nd edit


# @view_config( route_name='detail', renderer='string' )    # original swapped for 3rd edit
@view_config(route_name='detail', renderer='templates/detail.jinja2')    # 3rd edit
def view(request):    # no change
    this_id = request.matchdict.get('id', -1)    # 2nd edit
    entry = Entry.by_id(this_id)    # 2nd edit
    if not entry:    # 2nd edit
        return HTTPNotFound()    # 2nd edit
    return {'entry': entry}    # 2nd edit
    # return 'detail page'    # 1st edit


# @view_config(route_name='action', match_param='action=create', renderer='string')    # 4th edit swap with line below
@view_config(route_name='action', match_param='action=create',
            renderer='templates/edit.jinja2',
            permission='create')    # 4th edit
def create(request):    # no change
    entry = Entry()    # 2nd edit
    form = EntryCreateForm(request.POST)    # 2nd edit
    if request.method == 'POST' and form.validate():    # 2nd edit
        form.populate_obj(entry)    # 2nd edit
        DBSession.add(entry)    # 2nd edit
        return HTTPFound(location=request.route_url('home'))    # 2nd edit
    # return 'create page'    # 4th edit swap with return below
    return {'form': form, 'action': request.matchdict.get('action')}    # 4th edit


@view_config(route_name='action', match_param='action=edit',
            renderer='templates/edit.jinja2',
            permission='edit')
def update(request):
    # return 'edit page'    # no change. Commented out for Session2 homework
    id = int(request.params.get('id', -1))   # this looks in the query parameters to get the id
    entry = Entry.by_id(id)
    if not entry:
        return HTTPNotFound()
    form = EntryEditForm(request.POST, entry)    # the entry argument is an instance of the Entry.by_id
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)    # takes the data out of the form and puts it back into the object. It's already part of the db sessino, so you're don.
        return HTTPFound(location=request.route_url('detail', id=entry.id))
    return {'form': form, 'action': request.matchdict.get('action')}    # this returns the form with the title and body





conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_learning_journal_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""

