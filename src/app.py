import os
import sys
import bottle
from bottle import get
from bottle import run
from bottle import request
from bottle import static_file
from beaker.middleware import SessionMiddleware
import random

WWW_ROOT = os.path.join(os.path.dirname(__file__), '..', 'www')
SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 60 * 60 * 5,
    'session.data_dir': os.path.join(WWW_ROOT, 'session'),
    'session.auto': True
}


@get('/lucky')
def lucky():
    upload_path = os.path.join(WWW_ROOT, 'upload')
    files = filter(lambda e: not e.startswith('.'), os.listdir(upload_path))
    session = request.environ.get('beaker.session')
    luckers = session.setdefault('luckers', [])
    while 1:
        if not files or len(luckers) == len(files):
            return None
        lucky_file = files[random.randrange(0, len(files))]
        if lucky_file in luckers:
            continue
        luckers.append(lucky_file)
        session['luckers'] = luckers

        return 'upload/' + lucky_file


@get('/')
def index():
    return static('index.html')


@get('/static/:file_path#\S+#')
def static(file_path):
    root, file_name = os.path.split(file_path)
    return static_file(file_name, root=os.path.join(WWW_ROOT, root))


def run_app(port=8080):
    ''' start the app '''
    app = SessionMiddleware(bottle.app(), SESSION_OPTS)
    return run(app=app, host='0.0.0.0', port=port)


if __name__ == '__main__':
    run_app(sys.argv[1])
