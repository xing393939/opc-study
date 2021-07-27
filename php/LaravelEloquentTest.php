<?php

class EloquentBuilder
{
    // 定义查询所需要的参数
    protected $model;
    protected $wheres;
    protected $limit = 5;
    protected $columns;

    public function __construct(Model $model)
    {
        $this->model = $model;
    }

    // 根据上面的一些条件拼装sql
    public function toSql()
    {
        // 这里实现步骤大家可以自己去拼写
        $sql = json_encode([$this->columns, $this->wheres, $this->limit]);
        return $sql;
    }

    public function get($columns = ['*'])
    {
        $this->columns = $columns;

        // 执行mysql语句
        $results = $this->toSql();

        return $results;
    }

    // 设置参数
    public function take($value)
    {
        $this->limit = $value;
        return $this;
    }

    public function first($columns)
    {
        return $this->take(1)->get($columns);
    }

    public function where($column, $operator = null, $value = null)
    {
        $this->wheres[] = compact(
            'type', 'column', 'operator', 'value'
        );

        return $this;
    }

    public function find($id, $columns = ['*'])
    {
        return $this->where($this->model->primaryKey, '=', $id)->first($columns);
    }
}

class Model
{
    public function __call($method, $parameters)
    {
        $builder = new EloquentBuilder($this);
        return $builder->$method(...$parameters);
    }

    public static function __callStatic($method, $parameters)
    {
        return (new static)->$method(...$parameters);
    }
}

class Article extends Model
{
    public $primaryKey = 'id';
}

echo Article::find(1) . PHP_EOL;
echo Article::where('id', '>', 1)->get(['title']) . PHP_EOL;
