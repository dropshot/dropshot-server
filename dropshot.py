from bottle import route, run, template
import models

@route('/')
def hello():
    return "Wassup, yo?"

@route('/db')
def create_db():
    return models.session.query(models.Player).all()[0].to_json()
