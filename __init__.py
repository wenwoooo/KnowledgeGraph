from tools.database_neo4j.super_neo4j import DatabaseNeo4j

if __name__ == '__main__':
    db = DatabaseNeo4j()
    db.get_graph().delete_all()
