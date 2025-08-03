import re

from tools.file_help import file_with_json
from tools.database_neo4j.super_neo4j import DatabaseNeo4j
from py2neo import Node, Relationship
from configurations.key_label_match import *

keys = (('名称', MedicineName), ('俗名', CommonName), ('来源', Source), ('功能主治', Effect), ('性味', Taste),
        ('苗药名', MiaoMedicineName))

exist_Taste = True


def process_all_keys():
    db = DatabaseNeo4j()
    dic = file_with_json.open_file('./苗族常用植物药.json')
    for item in dic:
        print(item)
        p1 = db.add(MedicineName, name=item['名称'])
        p1['source'] = item['来源']
        db.push(p1)
        process_multiple(db, p1, Alias, CommonName, item['俗名'])
        process_miao_name(db, p1, item['苗药名'])
        process_nature_taste(db, p1, item['性味'])
        process_multiple(db, p1, Effect, Treatment, item['功能主治'])
        # p4 = Node(Taste, name=item[''])
        # Relationship()
    db.commit()


def process_miao_name(db: DatabaseNeo4j, p1, temp: str):
    for item in temp.split('、'):
        find = re.findall(r'([a-zA-Z ]*?) ([\u4e00-\u9fa5]+)(?:（([\u4e00-\u9fa5]+)）)?', item)
        if len(find) <= 0:
            print('--->', find)
        else:
            print('--->', find)
            find = find[0]
            p = db.add(Alias, name=find[1])
            p['place'] = find[2]
            db.push(p)
            s = db.add(Sound, name=find[0])
            db.create(Relationship(p, Pronunciation, s))
            db.create(Relationship(p1, MiaoMedicineName, p))


def process_nature_taste(db, p1, temp: str):
    if temp.find('味') == -1:
        exist_Taste = False
    temp = temp.split('性')
    process_multiple(db, p1, Taste, Taste, temp[0][1:])
    # print('味', temp[0][1:])
    if len(temp) > 1:
        process_multiple(db, p1, Speciality, Speciality, temp[1])
        # print('性', temp[1])


def process_multiple(db, p1, label, relationship, temp: str):
    for item in temp.split('、'):
        if item is None or len(item) == 0:
            continue
        # print(item)
        p = db.add(label, name=item)
        db.create(Relationship(p1, relationship, p))
