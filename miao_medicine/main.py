import re

from py2neo import Relationship, Node
from configurations.key_label_match import *
from tools.database_neo4j.super_neo4j import DatabaseNeo4j
from pandas import DataFrame
from tools.file_help import file_with_csv


# preprocess
# 病症表现
def process_behave(db: DatabaseNeo4j):
    pf = file_with_csv.open_file('./苗族医学/behave.csv')
    for item in pf.get('name'):
        # print(pf.get(key).to_string())
        print(item)
        if db is not None:
            db.add(Symptom, name=item)
    # db.commit()
    # print(pf)


# ?冷经冷病
def process_belong(db):
    pf = file_with_csv.open_file('./苗族医学/belongTo.csv')
    for item in pf.get('name'):
        print(item)
        if db is not None:
            db.add(Classification, name=item)
    # db.commit()


# 治疗方法,化痰 废弃
# def process_treatment(db: DatabaseNeo4j):
#     pf = file_with_csv.open_file('./苗族医学/treatment.csv')
#     for item in pf.get('name'):
#         print(item)
#         db.add(Effect, name=item)


# 正常处理
# id,name,miaoName,reason,describe
def process_disease(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('./苗族医学/disease.csv')
    for item in pf:
        print(type(item))
        _, name, miaoName, reasons, describe = item
        print(name, miaoName, reasons, describe)
        p = db.add(Disease, name=name, reasons=reasons, description=describe)
        ap = db.add(Alias, name=miaoName)
        db.create(Relationship(p, MiaoDiseaseName, ap))

    # print(pf)


# id,name,behave,belongTo,treatment,pharmacy
def process_pharmacy(db, p, prescriptions):
    # print(re.split('.方:', prescription))
    ''' 手动处理
    热经胄痛 鸡蛋壳100个，烘干为末，日服3~4次，每次3g
    热经腹痛 二方:珍姜（木姜子）6g,苞脚桑（地苦胆）6g,葛项嘎（鸡矢藤）12g,嘎龚珍宫幼（五香血藤）10g,隔山消10g,磨成细粉，每服2~4g,日服3次。
    热经串串咳 鸡苦胆1~2个，煎水加白糖服
    '''
    for t in re.split('.方:', prescriptions):
        if not (len(t) > 0):
            continue
        t = t.replace('。', '')
        t = t.replace('，', ',')
        properties = dict()
        if t.find('鸡苦胆1~2个') != -1:
            print('--->', t)
            continue

        prescription = t.split(',')
        pharmacy = []
        medicine = []
        for item in prescription[:-1]:
            find = re.findall(r'([A-Za-z|\u4e00-\u9fa5]+)(?:（([A-Za-z\u4e00-\u9fa5]*)）)?(\d*.{0,2}|适量)', item)
            if len(find) > 1 and len(find[1][0]) > 0:
                print('--->', find)
            elif len(find) > 0 and len(find[0][0]) > 0:
                # print('--->', find)
                name = find[0][0]
                usage = find[0][2]
                if len(find[0][1]) > 0:
                    name = find[0][1]
                    p1 = db.add(MedicineName, name=name)
                    medicine.append(p1)
                    mp = db.add(Alias, name=find[0][0])
                    db.create(Relationship(p1, MiaoMedicineName, mp))
                else:
                    p1 = db.add(MedicineName, name=name)
                    medicine.append(p1)
                pharmacy.append(f'{name}({usage})')
        p1 = db.add(Prescription, name='、'.join(pharmacy), usage=prescription[-1])
        for item in medicine:
            db.create(Relationship(p1, Include, item))
        db.create(Relationship(p, TreatmentWay, p1))


def process_illness_treatment(db: DatabaseNeo4j, p, treatment: str):
    treatment = treatment.replace('，', ',')
    treatment = treatment.replace('、', ',')
    for item in treatment.split(','):
        print(item)
        p1 = db.add(Effect, name=item)
        db.create(Relationship(p, TreatmentWay, p1))


def process_illness(db: DatabaseNeo4j):
    """
    strs = '一方:萬嘎得里（百部）10g,萬冲岗（白花蛇舌草）10g,萬灰萬菲（蒲公英）15g,榜佳腔（金银花）15g,萬祖别芭（白花前胡）10g,潘豆乃（十大功劳）1躍,煎水内服。二方:萬丢（折耳根）15g,佳洛浏吉（矮地茶）10&珍花休（瓜萎）10g,萬达赊芭（射干）10g,煎水内服。三方:潘豆莎（十大功劳）8g,珍佳俄董（麦冬）10g,萬祖别芭（前胡）10g,M久碧幼（一朵云）Wg,M相学（牛莠 子）12g,煎水内服。'
    print(re.split('.方:', strs))
    for item in re.split('.方:', strs):
        print(re.findall(r'(.*?)\（(.*?)\）.*?\\d*..+?', item))
    """
    pf = file_with_csv.open_file_to_numpy('./苗族医学/illness.csv')
    for item in pf:
        _, name, behave, belongTo, treatment, pharmacy = item
        # print(name, behave, belongTo, treatment, pharmacy)
        p = db.add(Illness, name=name)
        classification = db.add(Classification, name=belongTo)
        db.create(Relationship(p, Belong, classification))
        process_pharmacy(db, p, pharmacy)
        process_illness_treatment(db, p, treatment)


# id,name,miaoName,speciality,taste,type,function,useLevel
def process_medicine(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('./苗族医学/medicine.csv')
    for row in pf:
        _, name, miaoName, speciality, taste, type, function, useLevel = row
        print(name, miaoName, speciality, taste, type, function, useLevel)
        p = db.add(MedicineName, name=name)
        if miaoName != '无':
            mp = db.add(Alias, name=miaoName)
            db.create(Relationship(p, MiaoMedicineName, mp))
        sp = db.add(Speciality, name=speciality[1:])
        db.create(Relationship(p, Speciality, sp))
        for item in re.split('[，,]', taste):
            tt = db.add(Taste, name=item[1:])
            db.create(Relationship(p, Taste, tt))
        ty = db.add(MedicineType, name=type)
        db.create(Relationship(p, Belong, ty))
        for item in re.split('[，,]', function):
            ef = db.add(Effect, name=item)
            db.create(Relationship(p, Treatment, ef))


# 病与病症关联
# pre:process_illness
def process_rBehave(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('./苗族医学/rBehave.csv')
    for row in pf:
        print(row)
        p1 = db.evaluate(Illness, name=row[0])
        p2 = db.evaluate(Symptom, name=row[1])
        db.create(Relationship(p1, Cause, p2))


# 肺家咳嗽症,肺家热症咳嗽,include
# pre:process_disease、process_illness
def process_rInclude(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('./苗族医学/rInclude.csv')
    for row in pf:
        print(row)
        p1 = db.evaluate(Disease, name=row[0])
        p2 = db.evaluate(Illness, name=row[1])
        db.create(Relationship(p1, Include, p2))
