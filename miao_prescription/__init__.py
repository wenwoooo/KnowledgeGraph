from preprocess_data.miao_prescription import main
from tools.database_neo4j.super_neo4j import DatabaseNeo4j
import pandas as pd

if __name__ == '__main__':
    db = DatabaseNeo4j()
    # db = None
    # main.process_to_cvs(db)
    # main.process_csv_belong(db)
    main.process_csv_effect(db)
    db.commit()
    main.process_csv_interpretation(db)
    db.commit()
    # ppd = pd.DataFrame([['Sacramento', 'California']], columns=['City', 'State'])
    # ppd = ppd.add(pd.DataFrame([['Sacramento1', 'California1']], columns=['City', 'State']))
    # print(ppd)
