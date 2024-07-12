### Elasticsearch 基础

#### 参考资料
* [Elasticsearch复杂查询语法总结](https://juejin.cn/post/6998403625982623780)
* [ElasticSearch 中的 Mapping](https://codeshellme.github.io/2021/02/es-mappings/)
* [ES系列06：ik分词+Full text queries](https://cloud.tencent.com/developer/article/1746883)

#### 查询语法
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

// select * from user where name="wxx" or age =26
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

// select * from user where name="liujing" and age =18
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