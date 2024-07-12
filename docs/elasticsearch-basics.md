### Elasticsearch 基础

#### 参考资料
* [Elasticsearch复杂查询语法总结](https://juejin.cn/post/6998403625982623780)
* [Elasticsearch Index APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices.html)
* [ES系列06：ik分词+Full text queries](https://cloud.tencent.com/developer/article/1746883)

#### 查询语法
* [Elasticsearch Query Examples – Hands-on Tutorial](https://coralogix.com/blog/42-elasticsearch-query-examples-hands-on-tutorial/)
* [用法图表](../images/elasticsearch-query-guide.jpg)

```
// select * from user where name="wxx"
{
  "query": {
    "term": {
      "name": {
        "value": "wxx"
      }
    }
  }
}

// select * from user where address="抚州" 这里的match支持分词
{
  "query": {
    "match": {
      "address": {
        "value": "抚州"
      }
    }
  }
}

// select * from user where name in ("wxx", "zhangxianbo")
{
  "query": {
    "terms": {
      "name": [
        "zhangxianbo",
        "wxx"
      ]
    }
  }
}

// select * from user where age between 10 and 26
{
  "query": {
    "range": {
      "age": {
        "gte": 10,
        "lte": 26
      }
    }
  }
}

// select * from user where name="wxx" or age=26
{
  "query": {
    "bool": {
      "should": [
        {
          "term": {
            "name": {
              "value": "wxx"
            }
          }
        },
        {
          "term": {
            "age": {
              "value": "26"
            }
          }
        }
      ]
    }
  }
}

// select * from user where name="liujing" and age=18
{
  "query": {
    "bool": {
      "must": [
        {
          "term": {
            "name": {
              "value": "liujing"
            }
          }
        },
        {
          "term": {
            "age": {
              "value": "18"
            }
          }
        }
      ]
    }
  }
}
```

#### Mapping
* [ElasticSearch 中的 Mapping](https://codeshellme.github.io/2021/02/es-mappings/)
* ES 中的 Mapping 相当于传统数据库中的表定义
* 创建索引时，request body的mappings.properties下是字段定义