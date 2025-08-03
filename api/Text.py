from flask import Blueprint, request, make_response, session

api = Blueprint('test', __name__)


@api.route('/test/<int:id>')
def get(id):
    session['id'] = id
    print(id)
    return 'Hello World!'


@api.route('/send-message', methods=['POST'])
def send_question():
    print(session['id'])
    text = request.form.get('text')
    print(text)
    return 'ok'
