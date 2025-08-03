import re
import numpy as np

from tools.file_help.file_with_csv import CsvWriter
from tools.file_help import file_with_json, file_with_csv
from tools import is_null, dict_exist_key, is_str
from tools.database_neo4j.super_neo4j import DatabaseNeo4j
from py2neo import Node, Relationship
from configurations.key_label_match import *


# pharmacy_path = './data/.csv'
# prescription_index = 0


def process_miao_prescription(pre, pre_label, usage, prescriptions: str, db: DatabaseNeo4j):
    # global prescription_index
    # print(prescriptions)
    prescriptions = prescriptions.replace('。', '')
    prescriptions = prescriptions.replace('，', ',')
    prescriptions = prescriptions.replace(' ', '')
    container = []
    t = []
    for medicine in prescriptions.split(','):
        finds = re.findall(r'([A-Za-z|\u4e00-\u9fa5]+)(?:（([A-Za-z\u4e00-\u9fa5]*)）)?([\d~]*.{0,3}|适量)', medicine)
        if len(finds) > 0:
            # t = [f'P{prescription_index}']
            # print(finds)
            # for item in finds[0]:
            #     t.append(item)
            # container.append(t)
            print(medicine, finds)
            p = None
            if is_null(finds[0][1]):
                p = db.add(MedicineName, name=finds[0][0])
                t.append(f'{finds[0][0]}({finds[0][2]})')
            else:
                p = db.add(MedicineName, name=finds[0][1])
                mp = db.add(Alias, name=finds[0][0])
                db.create(Relationship(p, MiaoMedicineName, mp))
                t.append(f'{finds[0][1]}({finds[0][2]})')
            container.append(p)

        processed_str = ','.join((f'{item[0]}{f"（{item[1]}）" if item[1] != "" else ""}{item[2]}' for item in finds))
        # print(processed_str)
        if processed_str != medicine:
            pass
            # print(finds)
            # print('--->', processed_str, medicine, sep='|')
    if len(t) == 0:
        return
    p = db.add(Prescription, name='、'.join(t))
    for medicine in container:
        db.create(Relationship(p, Include, medicine))
    if not is_null(usage):
        p['usage'] = usage
        db.push(p)
    pp = db.add(pre_label, name=pre)
    db.create(Relationship(pp, TreatmentWay, p))
    # prescription_index += 1
    # print(prescription_index)
    # print(container)


# temp = False


def process_interpret_prescription(interpretation: str, csv_writer: CsvWriter):
    # print(interpretation)
    for item in re.split('[;；]', interpretation):
        # 清洗数据
        finds = re.split('[,，:。：]', item.strip('。'))
        for i in range(len(finds)):
            finds[i] = finds[i].strip()
        # for medicine in finds:
        #     if (medicine.find('性') != -1 and medicine.find('味') != -1) or (
        #             medicine.find('味') != -1 and medicine.find('属') != -1) or (
        #             medicine.find('属') != -1 and medicine.find('入') != -1) or (
        #             medicine.find('入') == -1 and medicine.find('经') != -1 and
        #             medicine.find('属两经药') == -1 and medicine.find('通经') == -1 and medicine.find('疏经') == -1
        #             and medicine.find('调经') == -1):
        #         print(interpretation)
        #         print('--->', medicine, finds)
        # 数据检查
        # t = 0
        # for medicine in finds:
        #     if medicine.find('性') != -1:
        #         if t > 0:
        #             print(medicine, finds)
        #             temp = True
        #             break
        #         else:
        #             t += 1
        #     if medicine.find('味') != -1:
        #         if t > 1:
        #             print(medicine, finds)
        #             temp = True
        #             break
        #         else:
        #             t += 1
        #     if medicine.find('属') != -1:
        #         if t > 2:
        #             print(medicine, finds)
        #             temp = True
        #             break
        #         else:
        #             t += 1
        #     if medicine.find('入') != -1:
        #         if t > 3:
        #             print(medicine, finds)
        #             temp = True
        #             break
        #         else:
        #             t += 1
        #     if medicine.find('有') != -1:
        #         if t > 4:
        #             print(medicine, finds)
        #             temp = True
        #             break
        #         else:
        #             t += 1

        # 数据处理
        if len(finds) > 1:
            row = [finds[0]]
            j = 1
            pattern = '性味属入有'
            save = ''
            for i in range(5):
                if j >= len(finds):
                    break
                if i != 4 and '有' in finds[j]:
                    save = finds[j][1:]
                    j += 1
                if pattern[i] in finds[j]:
                    row.append(finds[j][1:])
                    j += 1
                elif i != 4:
                    row.append('')
                else:
                    row.append(save)
            row.append('、'.join(finds[j:]))
            csv_writer.write_row(row)
            # print(row)


def process_treatment(pre, effects: str, csv_writer: CsvWriter):
    if is_null(effects):
        return
    effects = effects.replace('。', '')
    for item in re.split('[,，]', effects):
        print(item)
        for medicine in re.findall(r'([a-zA-Z \w-]*?)([\u4e00-\u9fa5]+)(?:（([\u4e00-\u9fa5]+)）)?', item.strip()):
            if len(medicine) < 3:
                continue
            t = list(medicine)
            if is_null(t[0]) and is_null(t[2]):
                k = t[1]
                t[1] = t[2]
                t[2] = k
            elif not is_null(t[0]) and is_null(t[2]):
                t[2] = t[1]
            for i in range(3):
                t[i] = t[i].strip()
            t.insert(0, pre)
            csv_writer.write_row(t)


def process_belong_to(belongs: str, pre, csv_writer: CsvWriter):
    if is_null(belongs):
        return
    print(pre, belongs)
    sp = re.split('属', belongs.strip('。').strip())
    sp.insert(0, pre)
    if len(sp) > 3:
        print('--->', sp)
    else:
        csv_writer.write_row(sp)


def storey(dic, pre, pre_label, csv_writer: CsvWriter, db: DatabaseNeo4j):
    if pre is None:
        print('--->', dic.get('child'))
    if 'child' in dic.keys():
        for key in dic['child']:
            label = Illness if key.find('方剂') == -1 else Formula
            p = key
            if p == '内治法' or p == '外治法（敷药）':
                print(p)
                p = pre
            mp = None
            # if 'alias' in dic[key].keys():
            if dict_exist_key(dic[key], 'alias'):
                print(dic[key]['alias'])
                try:
                    mp = db.add(Alias, name=key)
                    sound = db.add(Sound, name=dic[key]['alias'][0])
                    db.create(Relationship(mp, Pronunciation, sound))
                    p = dic[key]['alias'][1]
                except:
                    p = key
                    print('--->', dic[key]['alias'])

            v = db.add(pre_label, name=pre)
            u = db.add(label, name=p)
            db.create(Relationship(v, Include, u))
            if mp is not None:
                db.create(Relationship(v, MiaoDiseaseName, mp))
            if dict_exist_key(dic[key], 'title'):
                u['title'] = ''.join(dic[key]['title'])
                db.push(u)
            storey(dic[key], p, label, csv_writer, db)
    else:
        # print(dic['data'])
        for pharmacy in dic['data']:
            prescriptions = pharmacy['方剂']
            if prescriptions is None or len(prescriptions) == 0 or prescriptions == "None":
                continue
            process_miao_prescription(pre, pre_label, pharmacy['用法'], pharmacy['方剂'], db)
            # process_belong_to(pharmacy['属经'], pre, csv_writer)  # TODO need to process csv file
            # process_treatment(pre, pharmacy['治则'].strip(), csv_writer)  # TODO need to process csv file
            # process_interpret_prescription(pharmacy['方解'], csv_writer) # TODO need to process csv file


def process_to_cvs(db: DatabaseNeo4j):
    dic = file_with_json.open_file('./苗药方剂学.json')
    csv_writer1 = CsvWriter('./interpretation.csv',
                            ['name', 'speciality', 'taste', 'medicine type', 'passing', 'have', 'effect'])

    csv_writer2 = CsvWriter('./effect.csv', ['illness', 'sound', 'alias', 'effect'])
    csv_writer3 = CsvWriter('./belongTo.csv', ['illness', 'symptom', 'belong'])
    for key in dic['child']:
        if key == '外治法方剂':  # TODO 单独处理
            continue
        # TODO create formula. replace pre(None)
        p = db.add(Formula, name=key)
        if dict_exist_key(dic[key], 'title'):
            p['title'] = ''.join(dic[key]['title'])
            db.push(p)
        storey(dic[key], key, Formula, csv_writer3, db)
    # csv_writer3.fresh()
    # csv_writer2.print_()
    # print('---> temp ', temp)


def process_csv_effect(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('effect.csv')
    for row in pf:
        _, illness, sound, alias, effect = row
        print(illness, sound, alias, effect)
        ill = db.add(Illness, name=illness)
        p_effect = db.add(Effect, name=effect)
        db.create(Relationship(ill, TreatmentWay, p_effect))
        if is_str(alias):
            p_alias = db.add(Alias, name=alias)
            db.create(Relationship(p_effect, MiaoEffectName, p_alias))  # TODO 数据库添加错误，应重新添加
            if is_str(sound):
                p_sound = db.add(Sound, name=sound)
                db.create(Relationship(p_alias, Pronunciation, p_sound))


def process_csv_interpretation(db: DatabaseNeo4j):
    pf = file_with_csv.open_file_to_numpy('./interpretation.csv')

    count = 0

    for row in pf:
        _, name, speciality, taste, medicine_type, passing, have, effect = row
        print(name, speciality, taste, medicine_type, passing, have, effect)
        s_name = re.findall(r'([a-zA-Z -]*)([\u4e00-\u9fa5]+)（?([\u4e00-\u9fa5]*)）?', name)[0]
        print('--->', re.findall(r'([a-zA-Z -]*)([\u4e00-\u9fa5]+)（?([\u4e00-\u9fa5]*)）?', name)[0])
        p = None
        if not is_null(s_name[2]):
            p = db.add(MedicineName, name=s_name[2])
            alias = db.add(Alias, name=s_name[1])
            db.create(Relationship(p, MiaoMedicineName, alias))
        else:
            p = db.add(MedicineName, name=s_name[1])
        if not is_null(s_name[0]):
            sound = db.add(Sound, name=s_name[0])
            db.create(Relationship(p, Pronunciation, sound))

        if is_str(speciality):
            for item in speciality.split('、'):
                p_item = db.add(Speciality, name=item)
                db.create(Relationship(p, Speciality, p_item))

        if is_str(taste):
            for item in taste.split('、'):
                p_item = db.add(Taste, name=item)
                db.create(Relationship(p, Taste, p_item))

        if is_str(medicine_type):
            p_type = db.add(MedicineType, name=medicine_type)
            db.create(Relationship(p, Belong, p_type))

        if is_str(passing):
            for item in passing.split('、'):
                if not is_null(item):
                    p_pass = db.add(Classification, name=item)
                    db.create(Relationship(p, Passing, p_pass))

        if is_str(have):
            p_have = db.add(Taste, name=have)
            db.create(Relationship(p, Taste, p_have))

        if is_str(effect) and not is_null(effect):
            for item in re.split('、', effect):
                item.strip()
                if is_null(item):
                    continue
                finds = re.findall(r'([a-zA-Z ]*)([\u4e00-\u9fa5]+)（?([\u4e00-\u9fa5]*)）?', item)
                if len(finds) == 0:
                    continue
                s_item = finds[0]
                print(s_item)

                if not is_null(s_item[2]):
                    effect = db.add(Effect, name=s_item[2])
                    alias = db.add(Alias, name=s_item[1])
                    sound = db.add(Sound, name=s_item[0])
                    db.create(Relationship(p, Treatment, effect))
                    db.create(Relationship(effect, MiaoEffectName, alias))
                    db.create(Relationship(alias, Pronunciation, sound))
                else:
                    effect = db.add(Effect, name=s_item[1])
                    db.create(Relationship(p, Treatment, effect))

        count += 1
        if count == 500:
            count = 0
            db.commit()
            print('--------------------------------------------------------------------------------------')


def process_csv_belong(db: DatabaseNeo4j):  # TODO 之后处理
    pf = file_with_csv.open_file_to_numpy('./belongTo.csv')

    for row in pf:
        _, name, symptom, belong = row
        print(name, symptom, belong)
        # print(re.findall(r'([\u4e00-\u9fa5（）]*)（?([a-zA-Z ]*)([\u4e00-\u9fa5]*)）?', name))
        # print(re.findall(r'([\u4e00-\u9fa5（）]*)（?([a-zA-Z ]*)([\u4e00-\u9fa5]*)）?', name))
        if type(symptom) is str or not np.isnan(symptom):
            print(re.split(r'[,、，]', symptom))
