import uuid

from flask import Blueprint, request, session, make_response

from QA import QAContextManager

api = Blueprint('chat-robot', __name__)

# TODO resolve robot chat question
qa = QAContextManager('assets/chat-record', 'assets/static/classificier-relu-08.pth', 'assets/static')


# ner = NamedEntityRecognition(get_label_ac('../QA/data/recognition_label'))
# ir = IntentionRecognition('../QA/BertClassifier/classificier-relu-08.pth')


@api.route('/robot-init')
def robot_init():
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
    session_id = session.get('session')
    print(session_id, request.headers, request.cookies, session)
    qa.set(session_id)
    # g.robot = QABot(ner, ir)
    res = make_response(
        '你好，我是AI苗医药问答机器人。你可以输入药名、症状、疾病名称，我会尽我所能帮助你。' + '例如：\n什么药能清热解毒？\n痰液色黄是什么病？\n介绍一下一串红？')
    # res.set_cookie('SiteSame', 'None')
    return res


@api.route('/robot', methods=['POST'])
def question_answer():
    if 'uuid' not in session:
        session['uuid'] = str(uuid.uuid4())
    session_id = session.get('session')
    question = request.form['question']
    print(session_id, question, request.cookies)
    return '\n'.join(qa.answer(session_id, question))
