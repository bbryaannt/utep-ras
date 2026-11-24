"""Exercise a running production container without sending contact messages."""
import gzip
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

origin = os.environ.get('TEST_ORIGIN', 'http://127.0.0.1:8080').rstrip('/')

def get(path, headers=None):
    try:
        response = urlopen(Request(origin + path, headers=headers or {}), timeout=10)
    except HTTPError as error:
        response = error
    return response.status, response.headers, response.read()

for path, expected in [('/', b'ROBOTICS.'), ('/about', b'ABOUT'),
                       ('/projects', b'PROJECTS.'), ('/contact', b'contact-form'),
                       ('/join', b'Join'), ('/rover', b'ROVER'),
                       ('/garage-occupancy-sensor', b'SENSOR'),
                       ('/rtx-competition', b'RTX'), ('/privacy', b'PRIVACY'),
                       ('/terms', b'TERMS'), ('/thanks.html', b'submitted')]:
    code, headers, body = get(path)
    assert code == 200 and expected in body, (path, code)
    assert headers.get('X-Content-Type-Options') == 'nosniff', path
    assert headers.get('Cache-Control') == 'no-cache', path

assert get('/healthz')[0::2] == (200, b'ok\n')
code, headers, body = get('/assets/rover-640.webp')
assert code == 200 and len(body) > 1000
assert 'max-age=86400' in headers.get('Cache-Control', '')
for path in ['/missing-container-test', '/missing/deep/page', '/Dockerfile', '/assets/missing.png']:
    code, _, body = get(path)
    assert code == 404 and b'Page not found' in body, path
code, headers, body = get('/', {'Accept-Encoding': 'gzip'})
assert headers.get('Content-Encoding') == 'gzip'
assert b'ROBOTICS.' in gzip.decompress(body)
print('PASS: routes, health, custom 404, compression, security headers and asset caching')
