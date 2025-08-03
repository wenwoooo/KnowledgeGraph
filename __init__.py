from abc import ABC
from datetime import datetime

from QA.AnalysisMechanism import AnalysisMechanism
from QA.BertClassifier import IntentionRecognition, BertClassifier, BertBiLSTMMixMSAClassifier
from QA.NamedEntityRecognition import NamedEntityRecognition
from configurations import network_port, network_address
from QA.data.recognition_label import get_label_ac
from tools import ContextManager
from tools import QAPServer


class QABot:
    def __init__(self, am: AnalysisMechanism, ner: NamedEntityRecognition, ir: IntentionRecognition):
        self.ir = ir
        self.ner = ner
        self.am = am

        self.chat_record = list()

    def question_answer(self, question: str) -> list:
        label_idx, label = self.analysis(question)
        parsers = self.parser(question)
        self.chat_record.append((question, (str(label_idx), label), parsers))
        return self.am.process(question, label_idx, parsers)

    def parser(self, text: str) -> dict[str, set]:
        return self.ner.parser(text)

    def analysis(self, text: str) -> (int, str):
        return self.ir.predict(text)

    def close(self, path, key: str = None):
        if len(self.chat_record) == 0:
            return
        file_name = f'{path}/session_{key if key is not None else "none"}_{datetime.now().timestamp()}.dat'
        with open(file_name, 'w', encoding='utf-8') as fp:
            for item in self.chat_record:
                fp.writelines(('1', ' ', item[0], '\n'))
                fp.writelines(('2', ' ', ' '.join(item[1]), '\t',
                               '\t'.join(f"{key}:{' '.join(values)}" for key, values in item[2].items()), '\n'))


class QAContextManager(ContextManager, ABC):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        for key, item in self.store.items():
            # print(key, item)
            item.close(self.chat_save_path, key)

    def __init__(self, record_path='./data/chat_record', module_path='./BertClassifier/classificier-relu-08.pth',
                 label_path='./data/recognition_label'):
        self.ner = NamedEntityRecognition(get_label_ac(label_path))
        self.ir = IntentionRecognition(module_path)
        self.am = AnalysisMechanism()
        self.store = dict[str, QABot]()

        self.chat_save_path = record_path

    def answer(self, key, question) -> list:
        if not self.exist_key(key):
            return [f'key:{key} does not exist']
        return self.store[key].question_answer(question)

    def push(self, key) -> QABot:
        if not self.exist_key(key):
            self.store[key] = QABot(self.am, self.ner, self.ir)
        return self.get(key)

    def pop(self, key) -> QABot:
        if self.exist_key(key):
            self.store[key].close(self.chat_save_path, key)
        return self.store.pop(key)

    def set(self, key):
        if self.exist_key(key):
            self.pop(key).close(self.chat_save_path, key)
        return self.push(key)

    def get(self, key, default: QABot = None) -> QABot:
        return self.store[key] if key in self.store else default

    def exist_key(self, key) -> bool:
        return key in self.store


if __name__ == '__main__':
    # key = 'ffff'
    # file_name = f'./data/chat_record/{key if key is not None else ""}{datetime.now().timestamp()}.dat'
    # print(file_name)
    # with open('test.txt', 'w', encoding='utf-8') as fp:
    #     s = set()
    #     s.add(('咳嗽', 'Effect'))
    #     s.add(('咳嗽', 'Symptom'))
    #     # print(s)
    #     print('\t'.join(':'.join(item) for item in s))
    #     fp.writelines(('ffff', '1', 'ffff', '\n\r'))
    #     fp.write('fff\tffff')
    #     fp.writelines('\t'.join(':'.join(item) for item in s))

    # with QAContextManager() as qa:
    #     qa.set('ffff')
    # print(qa.answer('ffff', '什么药能舒经通络、活血化瘀'))
    # print(qa.answer('ffff', '痰液色黄是什么病'))
    # print(qa.answer('ffff', '介绍一下一串红'))
    # print(qa.answer('ffff', '病因证治方剂'))
    # print(qa.answer('ffff', '我有些头痛'))
    # sv = QAPServer(network_address, network_port)
    # sv.start(lambda key, qst: '\n'.join(qa.answer(key, qst)))
    with QAContextManager() as qa:
        qa.set('test')
        for i in range(4):
            text = input("用户：")
            print("robot:", qa.answer('test', text), sep='')

    pass
