from webtest import TestApp
import dropshot


def test_create_player():
    app = TestApp(dropshot.app)

    params = {'username': 'chapmang',
              'password': 'deadparrot',
              'email': 'chapmang@dropshot.com'}

    expected = {'count': 1,
                'offset': 0,
                'players': [
                    {'gamesPlayed': 0,
                     'username': 'chapmang'}
                ]}

    app.post('/players', params)

    res = app.get('/players')

    assert res.status_int == 200
    assert res.content_type == 'application/json'
    assert res.json == expected
