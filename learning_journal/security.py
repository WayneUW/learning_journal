from pyramid.security import Allow, Everyone, Authenticated

class EntryFactory(object):
    __acl__ = [   # this is an action control list. Two valid actions - allow and deny
        (Allow, Everyone, 'view'),   # the principal is everyone, everyone is every request. the third item is what you can do
        (Allow, Authenticated, 'create'),    # authenticated is anyone who passes the everyone. If I am auth give me a permission
        (Allow, Authenticated, 'edit'), 
    ]
    def __init__(self, request):
        pass
