from webtest import TestApp
import dropshot

def test_create_player():
    app = TestApp(dropshot.app)
    params = {'username': 'chapmang',
              'password': 'deadparrot',
              'email': 'chapmang@dropshot.com'}

    app.post('/players', params)

    res = app.get('/players')

    assert res.status_int == 200
