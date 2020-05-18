import flask as f
import functools

from . import database

from http import HTTPStatus

def requireAuth(func=None, /, **factoryKwargs):
    AUTH_HEADER="token"
    if not func:
        return functools.partial(requireAuth)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            givenToken = f.request.headers[AUTH_HEADER]
        except KeyError:
            return (f'You must use the \"{AUTH_HEADER}\" header to authenticate', HTTPStatus.UNAUTHORIZED)

        givenDB = 'db' in kwargs
        if givenDB:
            db = kwargs['db']
        else:
            db = database.get_db()

        rows = db.execute('SELECT * FROM auth_token WHERE token = ?', (givenToken,)).fetchone()
        if rows is None or len(rows) == 0:
            return ("The provided auth token does not have access to this resource", HTTPStatus.FORBIDDEN)

        if not givenDB:
            db.commit()

        return func(*args, **kwargs)
    return wrapper
