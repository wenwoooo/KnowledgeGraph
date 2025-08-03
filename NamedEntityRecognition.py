from ahocorasick import Automaton, AHOCORASICK

from QA.data.recognition_label import get_label_ac


class NamedEntityRecognition:
    def __init__(self, ac_sicks: dict = None):
        self.ac_sicks = ac_sicks if ac_sicks is not None else {}

    def add_recognition_way(self, key: str, ac: Automaton):
        if ac.kind != AHOCORASICK:
            ac.make_automaton()
        self.ac_sicks[key] = ac

    def parser(self, text, *keys) -> dict[str, set]:
        pair = {}
        if keys is not None and len(keys) > 0:
            for key in keys:
                for _, res in self.ac_sicks[key].iter_long(text):
                    if key not in pair:
                        pair[key] = set()
                    pair[key].add(res)
            return pair
        for key, acc in self.ac_sicks.items():
            for _, res in acc.iter_long(text):
                if key not in pair:
                    pair[key] = set()
                pair[key].add(res)
        return pair


if __name__ == '__main__':
    ner = NamedEntityRecognition(get_label_ac('data/recognition_label'))
    print(ner.parser('医生，我有点咳嗽'))
