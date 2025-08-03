import main
import re

from configurations.key_label_match import *

from tools.database_neo4j.super_neo4j import DatabaseNeo4j

if __name__ == '__main__':
    db = DatabaseNeo4j()
    # main.process_behave(db)
    # main.process_belong(db)
    # pre
    # main.process_medicine(db)
    # main.process_illness(db)
    # main.process_disease(db)

    main.process_rBehave(db)
    main.process_rInclude(db)

    # print(db.evaluate(Classification, name='补气') is None)
    db.commit()
    # properties = dict()
    # properties['fadfad'] = 'fadf'
    # print(properties)
    # print(len(''))
    # prescription = '一方:仰抵嘎（沙参）8g,姜加莪董（麦冬）8g,波嘎梯（百合）8g,夜寒苏15g,煎水内服。二方:萬丢（白折耳）10g,M久碧幼（一朵云）奨,萬首扎（岩白菜）1源,蜂蜜适量,煎水内服。三方:仰抵嘎（沙参）10g,肝努净菸（岩SI豆）8g,佳珍嘎佬苑（果上叶）10g,波嘎梯（百合）,煎水内服。'
    # print(re.split('.方:', prescription))
    # for t in re.split('.方:', prescription):
    #     t = t.replace('。', '')
    #     for item in t.split(','):
    #         print(item)
    #         print(re.findall(r'([A-Za-z\u4e00-\u9fa5]*)(?:（([\u4e00-\u9fa5]*)）)?(\d*.?)', item))
    # strs = 'fa,法大师傅，dfa'
    # print(strs[1:])
    # print(re.split('[，,]', strs))
    # print(strs.split(','))
