毕业设计

```cypher
// 删除重复关系
MATCH (a)-[r:relationship]->(b)
WITH a, b, TAIL (COLLECT (r)) as rr
WHERE size(rr)>0
FOREACH (r IN rr | DELETE r)
```