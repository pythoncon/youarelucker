import os
import sys
import bottle
from bottle import get
from bottle import run
from bottle import static_file
import random

WWW_ROOT = os.path.join(os.path.dirname(__file__), '..', 'www')


@get('/lucky')
def lucky():
    upload_path = os.path.join(WWW_ROOT, 'upload')
    files = filter(lambda e: not e.startswith('.'), os.listdir(upload_path))
    if not files:
        return None
    lucky_file = files[random.randrange(0, len(files))]
    # hide lucky_file in next round
    new_lucky_file = '.' + lucky_file
    os.rename(os.path.join(upload_path, lucky_file), os.path.join(upload_path, new_lucky_file))

    return 'upload/' + new_lucky_file


@get('/')
def index():
    return static('index.html')


@get('/static/:file_path#\S+#')
def static(file_path):
    root, file_name = os.path.split(file_path)
    return static_file(file_name, root=os.path.join(WWW_ROOT, root))


def run_app(port=8080):
    ''' start the app '''
    return run(app=bottle.app(), host='0.0.0.0', port=port)


if __name__ == '__main__':
    run_app(sys.argv[1])
