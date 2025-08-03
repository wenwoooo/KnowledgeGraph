# 由于api更新，这里做了一些调整
import os

import flask_restful as restful
from flask import Flask
from flask_cors import CORS

from QA import BertClassifier, BertBiLSTMMixMSAClassifier
from api.ChatRobot import api as chat_api, qa
from api.Text import api as text_api
from api.search import api as search_api, db

# qa = QAContextManager('assets/chat-record', 'assets/static/classificier-relu-08.pth', 'assets/static')

app = Flask(__name__)
CORS(app)
# CORS(app, origins=['http://localhost:63343'], supports_credentials=True)
app.secret_key = os.urandom(24)

app.register_blueprint(text_api)
app.register_blueprint(chat_api)
app.register_blueprint(search_api)
api = restful.Api(app)

# with app.app_context():
# ner = NamedEntityRecognition(get_label_ac('../QA/data/recognition_label'))
# ir = IntentionRecognition('../QA/BertClassifier/classificier-relu-08.pth')

# global

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
    # TODO if setting chat robot context-manager in ChatRobot.py, please remember to close
    db.commit()
    qa.close()
