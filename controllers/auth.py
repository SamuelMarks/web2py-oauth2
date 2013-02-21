#!/usr/bin/python
# -*- coding: utf-8 -*-

from gluon.http import HTTP
from gluon.tools import Field
from gluon.sqlhtml import SQLFORM

def index():
    """
    This method has two functionalities:
    1. Asks the user if he permits that a 3rd party app access his data
    2. Receives the user's answer and redirect the user to the 3rd party
       correspondant URI
    In case of error, it redirects to the 'error' controller. 
    Of course, you can modify this behavior. For instance, you may want return
    a JSON or HTTP error instead.
    
    The request MUST be like this:
    http://[your_server]{:port}/[your_application]/auth?
    client_id=[your_client_id]&
    redirect_uri=[your_callback_uri]&
    response_type=code&
    access_type=online
    NOTE: You can pass a "scope" parameter, but you need to configure it at the
    OAuth2 object constructor.
    """
    
    from oauth.storage import web2pyStorage as storage  # change to MongoStorage if you aren't using DAL
    storage = storage()
    storage.connect()
    oauth = OAuth2(storage)
    
    # Validates GET parameters
    params = dict()
    success = False
    
    #try:
    params = oauth.validate_authorize_params(request.get_vars)
    #except Exception as ex:
    #    redirect(URL(c='error', vars=dict(msg=ex)))

    error = []
    client_id = params.get('client_id', error.append('No client_id'))
    redirect_uri = params.get('redirect_uri', error.append('No redirect_uri'))
    the_scope = params.get('scope', None)
    response_type = params.get('response_type', error.append('No response_type'))
    access_type = params.get('access_type', error.append('No access_type'))

    approval_form = SQLFORM.factory(submit_button='Yes')
    approval_form.add_button('No', redirect_uri + '#error=access_denied')
 
    if approval_form.process().accepted:
        user_id = '501faa19a34feb05890005c9' # Change to `auth.user` for web2py
        code = oauth.storage.add_code(client_id, user_id,
                                      oauth.config[oauth.CONFIG_CODE_LIFETIME])
        raise(404, 'redirect_uri ={0}'.format(redirect_uri))
        #redirect(redirect_uri + '?code={code}'.join(code=code))
    
    #print 'response_type =', response_type
    #print 'client_id =', client_id
    #print 'redirect_uri =', redirect_uri
    #print 'response_type =', response_type
    #print 'access_type =', access_type
    
    if error:
        print (412, 'KeyError(s): {0}'.format(', '.join(error)))
    
    url = '?client_id={client_id}&redirect_uri={redirect_uri}'
    url += '&response_type={response_type}&access_type={access_type}'
    url = url.format(client_id=client_id, redirect_uri=redirect_uri,
                     response_type=response_type, access_type=access_type)
    print 'url =', url

    return locals()

