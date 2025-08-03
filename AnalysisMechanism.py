from __future__ import annotations

from typing import Generator

from configurations.key_label_match import Illness, Cause, TreatmentWay, Belong, Prescription, Disease, Include, \
    Symptom, Effect, MedicineName, Treatment, Taste, Speciality, Passing, MiaoEffectName, Pronunciation, \
    MiaoDiseaseName, MiaoMedicineName, Formula
from tools import is_null
from tools.database_neo4j.super_neo4j import DatabaseNeo4j, get_label_name

"""
'病情诊断': 0,
'病因分析': 1,
'治疗方案': 2,
'就医建议': 3,
'指标解读': 4,
'疾病表述': 5,
'后果表述': 6,
'注意事项': 7,
'功效作用': 8,
'医疗费用': 9,
'其他': 10

Illness, Classification, MedicineName, Effect, Taste, Symptom, MedicineType, Formula, Disease
"""


def alias_name_(p, r, db: DatabaseNeo4j) -> str:
    alias = db.match([p], r).first()
    if alias is None:
        return p['name']
    alias = alias.end_node
    sound = db.match([alias], Pronunciation).first()
    if sound is None:
        return f"{p['name']}({alias['name']})"
    sound = sound.end_node
    return f"{p['name']}({sound['name']} {alias['name']})"


def illness_name_(p, db: DatabaseNeo4j) -> str:
    name = alias_name_(p, MiaoDiseaseName, db)
    return name if 'title' not in p else f"{name}，{p['title']}"


def effect_name_(p, db: DatabaseNeo4j) -> str:
    return alias_name_(p, MiaoEffectName, db)


def disease_name_(p, db: DatabaseNeo4j) -> str:
    name = alias_name_(p, MiaoDiseaseName, db)
    return f"{name}，" if 'description' not in p else f"{name}，{p['description']}"


def medicine_name_(p, db: DatabaseNeo4j) -> str:
    return alias_name_(p, MiaoMedicineName, db)


def formula_name_(p, db: DatabaseNeo4j) -> str:
    return alias_name_(p, MiaoDiseaseName, db)


def illness_answer(illness: str, db: DatabaseNeo4j) -> str:
    p = db.evaluate(Illness, name=illness)
    if p is None:
        return ''

    # 处理特殊情况
    res = formula_format(p, db)
    if not is_null(res):
        return res

    answer = []
    symptoms = (item.end_node['name'] for item in db.match([p], Cause).all())
    prescriptions = []
    effects = []
    for item in db.match([p], TreatmentWay).all():
        # print(get_label_name(item.end_node) == Prescription, get_label_name(item.end_node), item.end_node)
        if get_label_name(item.end_node) == Prescription:
            prescriptions.append(
                item.end_node['name'] + f'{"，" + item.end_node["usage"] if "usage" in item.end_node else ""}')
        else:
            effects.append(item.end_node['name'])
    classifications = (item.end_node['name'] for item in db.match([p], Belong).all())
    answer.append(
        f'{illness_name_(p, db)}，{p["title"] + "，" if "title" in p else ""}属{"、".join(classifications)}；病时{"、".join(symptoms)}；治法{"、".join(effects)}。')
    if len(prescriptions) != 0:
        answer.append(f'方药：{"；".join(prescriptions)}。')

    return '\n'.join(answer)


def disease_answer(disease, db: DatabaseNeo4j) -> str:
    p = db.evaluate(Disease, name=disease)
    if p is None:
        return ''
    includes = (item.end_node['name'] for item in db.match([p], Include).all())
    return f'{disease_name_(p, db)}{p["description"]}致病原因{p["reasons"]}又分为{names_join(includes)}'


def medicine_answer(medicine, db: DatabaseNeo4j) -> str:
    p = db.evaluate(MedicineName, name=medicine)
    if p is None:
        return ''

    answers = []
    tastes = db.match([p], Taste)
    specialities = db.match([p], Speciality)
    tsp = ''
    if specialities is not None and len(specialities) > 0:
        tsp = '性' + '、'.join(item.end_node['name'] for item in specialities)
    if tastes is not None and len(tastes) > 0:
        tsp += '味' + '、'.join(item.end_node['name'] for item in tastes)
    passing = db.match([p], Passing)
    if passing is not None and len(passing) > 0:
        tsp += '，归' + '、'.join(item.end_node['name'] for item in passing)
    if not is_null(tsp):
        answers.append(f'{medicine_name_(p, db)}，{tsp}')

    if 'source' in p:
        answers.append('来源：' + p['source'])

    effects = db.match([p], Treatment)
    # print(effects.all())
    if effects is not None and len(effects) != 0:
        answers.append('功效治疗：' + names_join(effect_name_(item.end_node, db) for item in effects))
    ills = list(db.run("match (p1:MedicineName {name: '" + medicine +
                       "'})<-[:Include]-(p3:Prescription)<-[:TreatmentWay]-(p2:Illness) return p2"))
    if ills is not None and len(ills) != 0:
        answers.append('主治：' + names_join(item['p2']['name'] for item in ills))
    return '\n'.join(answers)


def formula_format(p, db) -> str:
    includes = db.match([p], Include).all()
    if len(includes) != 0:
        return f"{formula_name_(p, db)}，{p['title']}\n其中包括：{names_join(formula_name_(item.end_node, db) for item in includes)}"
    return ''


def formula_answer(formula, db: DatabaseNeo4j) -> str:
    p = db.evaluate(Formula, name=formula)
    if p is None:
        return ''
    return formula_format(p, db)


def intersection_template(name_entities: set[str], label, relation, db: DatabaseNeo4j) -> set:
    res = set()
    for entity in name_entities:
        p = db.evaluate(label, name=entity)
        # print(db.match([None, p], relation).all())
        data = (item.start_node["name"] for item in db.match([None, p], relation))
        # print(list(data))
        if len(res) == 0:
            res.update(data)
        else:
            res = res.intersection(data)
    return res


def names_join(name_entities: list[str] | set[str] | Generator) -> str:
    if type(name_entities) is not list:
        name_entities = list(name_entities)
    names = "、".join(name_entities[:-1])
    if len(name_entities) > 1:
        names += '和'
    return names + name_entities[-1]


def symptom_answer(name_entities: set[str], db: DatabaseNeo4j) -> list[str]:
    if name_entities is None:
        return []
    symptoms = list(name_entities)
    if len(symptoms) == 0:
        return []
    symptom = names_join(symptoms)
    ills = intersection_template(name_entities, Symptom, Cause, db)
    if len(ills) == 0:
        return [f'抱歉，我不知道{symptom}会引起什么病。']
    return [f'{symptom}可能引起{names_join(ills)}。'] + diagnose_template(ills, db, illness_answer)


def effect_answer(name_entities: set[str], db: DatabaseNeo4j) -> list[str]:
    if name_entities is None:
        return []
    effects = list(effect_name_(db.evaluate(Effect, name=item), db) for item in name_entities)
    if len(effects) == 0:
        return []
    effect = names_join(effects)
    medicines = intersection_template(name_entities, Effect, Treatment, db)
    if len(medicines) == 0:
        return [f'抱歉，我没找到有{effect}功效的药。']
    return [f'有{effect}功效的药有：{names_join(medicines)}。']


def diagnose_template(name_entities: set[str], db: DatabaseNeo4j, process_act) -> list:
    answers = []
    if name_entities is None:
        return answers
    for item in name_entities:
        answer = process_act(item, db)
        if not is_null(answer):
            answers.append(answer)
    return answers


def illness_diagnose(question: str, label_idx: int, name_entities: dict[str, set], db: DatabaseNeo4j) -> str:
    return '\n'.join([*diagnose_template(name_entities.get(Illness), db, illness_answer),
                      *diagnose_template(name_entities.get(Disease), db, disease_answer),
                      *symptom_answer(name_entities.get(Symptom), db)])


def cause_diagnose(question: str, label_idx: int, name_entities: dict[str, set], db: DatabaseNeo4j) -> str:
    pass  # TODO cause_diagnose


def cure_way(question: str, label_idx: int, name_entities: dict[str, set], db: DatabaseNeo4j) -> str:
    return '\n'.join([*symptom_answer(name_entities.get(Symptom), db),
                      *effect_answer(name_entities.get(Effect), db),
                      *diagnose_template(name_entities.get(Illness), db, illness_answer)])


def effect_describe(question: str, label_idx: int, name_entities: dict[str, set], db: DatabaseNeo4j) -> str:
    return '\n'.join([*effect_answer(name_entities.get(Effect), db),
                      *diagnose_template(name_entities.get(MedicineName), db, medicine_answer)])


def others(question: str, label_idx: int, name_entities: dict[str, set], db: DatabaseNeo4j) -> str:
    return '\n'.join([*diagnose_template(name_entities.get(Illness), db, illness_answer),
                      *diagnose_template(name_entities.get(Disease), db, disease_answer),
                      *diagnose_template(name_entities.get(MedicineName), db, medicine_answer),
                      *diagnose_template(name_entities.get(Formula), db, formula_answer),
                      *symptom_answer(name_entities.get(Symptom), db)])


class AnalysisMechanism:
    def __init__(self):
        self.machine = StateMachine(0, illness_diagnose)
        self.machine.next(
            StateMachine(2, cure_way)).next(
            StateMachine(8, effect_describe)).next(
            StateMachine(10, others))
        self.db = DatabaseNeo4j()
        # self.state = {}

        self.diagnose = False
        self.symptoms = set()

    def diagnose_(self, question=None) -> list:
        # TODO 添加问诊模式
        pass

    def process(self, question: str, label_idx: int, parsers: dict[str, set]) -> list:
        res = None
        # if self.diagnose:
        #     if question == '是' or question == '否':
        #         self.symptoms.update(parsers[Symptom])
        #         res = self.diagnose_(question)
        #     else:
        #         self.diagnose = False
        #         self.symptoms.clear()

        label = label_idx

        # 重新映射问题类型
        if label == 1:
            label = 0
        if label == 3 or label == 4:
            label = 2
        if label == 5:
            label = 0

        if parsers is not None:
            res = self.machine(question, label, parsers, self.db)
        # 删除问诊模式
        # if not self.diagnose and parsers is not None:
        #     if len(parsers) == 1 and Symptom in parsers:
        #         self.diagnose = True
        #         self.symptoms.update(parsers[Symptom])
        #         res = self.diagnose_()
        #     else:
        #         res = self.machine(question, label, parsers, self.db)
        if res is None or len(res) == 0:
            return [f'抱歉我{"不明白你的意思" if label == 10 else "不知道你说的"}，你可以问些其他的。',
                    '例如：\n\t什么药能清热解毒？\n\t痰液色黄是什么病？\n\t介绍一下一串红？']
        return res


class StateMachine:
    def __init__(self, process_id, act=None):
        self.process_id = process_id
        self.next_item = None
        self.act = act

    def __call__(self, question: str, label_idx: int, parsers: dict, db: DatabaseNeo4j) -> list:
        res = []
        if self.handle(label_idx) and self.act is not None:
            re = self.act(question, label_idx, parsers, db)
            if not is_null(re):
                res.append(re)
        res.extend(self.forward(question, label_idx, parsers, db))
        return res

    def forward(self, question: str, label_idx: int, parsers: dict, db: DatabaseNeo4j) -> list:
        if self.next_item is not None:
            return self.next_item(question, label_idx, parsers, db)
        return []

    def next(self, next_item=None):
        self.next_item = next_item
        return next_item

    def handle(self, process_id):
        return self.process_id == process_id


if __name__ == '__main__':
    # ner = NamedEntityRecognition(get_label_ac('./data/recognition_label'))
    # tmp = []
    # text = '医生，我有点咳嗽'
    # illness_diagnose(text, 0, tmp, ner, None)
    pass
