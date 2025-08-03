# label name
Formula = 'Formula'  # 方剂
MedicineName = 'MedicineName'  # 药名
Alias = 'Alias'  # 别名
Effect = 'Effect'  # 功效
Prescription = 'Prescription'  # 药方
Classification = 'Classification'  # 分类：方剂，部，经
Symptom = 'Symptom'  # 症状
Disease = 'Disease'  # 大疾病
Illness = 'Illness'  # 疾病
Reason = 'Reason'  # 病因
Sound = 'Sound'  # 拼音
MedicineType = 'MedicineType'  # 两经药，冷药，热药

# relationship
Treatment = 'Treatment'  # 治疗
TreatmentWay = 'TreatmentWay'  # 治疗方法
Include = 'Include'
Belong = 'Belong'
Passing = 'Passing'  # 经过，入冷经、热经……
CommonName = 'CommonName'  # 俗名
MiaoMedicineName = 'MiaoMedicineName'  # 苗药名
AnotherName = 'AnotherName'  # 别名
Cause = 'Cause'  # 由xx引起
MiaoDiseaseName = 'MiaoDiseaseName'  # 苗病名
MiaoEffectName = 'MiaoEffectName'  # 苗 效果 名 hxub hxab kib caf net旭嘎凯滁内（清热消肿）
Pronunciation = 'Pronunciation'  # 发音

# common
Source = 'Source'  # 来源
Taste = 'Taste'  # 味
Speciality = 'Speciality'  # 性

rev_name = {
    'All': '全部',
    MedicineName: '药名',
    Formula: '方剂',
    Alias: '别名',
    Effect: '功效',
    Symptom: '症状',
    Illness: '疾病',  # include 'Disease' and 'Illness'
    Sound: '读法'
}

rev_relationship = {
    Treatment: '治疗',
    TreatmentWay: '治疗方法',
    Include: '包含',
    Belong: '属于',
    Passing: '经过',
    CommonName: '俗名',
    MiaoMedicineName: '苗名',
    AnotherName: '别名',
    Cause: '引起',
    MiaoDiseaseName: '苗名',
    MiaoEffectName: '苗名',
    Pronunciation: '发音',
    Source: '来源',
    Taste: '味',
    Speciality: '性'
}

NeedLabel = [Illness, MedicineName, Effect, Taste, Symptom, MedicineType, Formula, Disease]

labels = {'病情诊断': 0,
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
          }
rev_labels = ['病情诊断', '病因分析', '治疗方案', '就医建议', '指标解读', '疾病表述', '后果表述', '注意事项',
              '功效作用', '医疗费用', '其他']
