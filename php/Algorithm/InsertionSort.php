<?php


class InsertionSort
{
    static function sort($arr)
    {
        $n = count($arr);
        for ($i = 1; $i < $n; $i++) {
            $value = $arr[$i];
            for ($j = $i - 1; $j >= 0; $j--) {
                if ($arr[$j] > $value) {
                    $arr[$j + 1] = $arr[$j];
                } else {
                    break;
                }
            }
            $arr[$j + 1] = $value;
        }

        return $arr;
    }
}

$arr = [8, 15, 3, 102, 6, 46, 11];
echo json_encode(InsertionSort::sort($arr));