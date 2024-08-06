from elasticsearch import Elasticsearch

# 创建 Elasticsearch 客户端
es = Elasticsearch(
    ["http://localhost:9200"]
   
)

# 创建索引
index_name = 'my_index4'
es.indices.create(index=index_name)

# 插入数据
doc = {
    'author': 'John Doe',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': '2024-08-02T14:12:12'
}
res = es.index(index=index_name, id=1, document=doc)
print(res['result'])

# 查询数据
res = es.get(index=index_name, id=1)
print(res['_source'])