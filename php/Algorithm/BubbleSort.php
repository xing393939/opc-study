<?php


class BubbleSort
{
    static function sort($arr)
    {
        $n = count($arr);
        for ($i = 0; $i < $n; $i++) {
            for ($j = 1; $j < $n - $i; $j++) {
                if ($arr[$j] < $arr[$j - 1]) {
                    $tmp = $arr[$j];
                    $arr[$j] = $arr[$j - 1];
                    $arr[$j - 1] = $tmp;
                }
            }
        }

        return $arr;
    }
}

$arr = [8, 15, 3, 102, 6, 46, 11];
echo json_encode(BubbleSort::sort($arr));