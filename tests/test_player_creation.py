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

    post_response = app.post('/players', params)
    assert post_response.status_int == 201

    get_response = app.get('/players')
    assert get_response.status_int == 200
    assert get_response.content_type == 'application/json'
    assert get_response.json == expected
