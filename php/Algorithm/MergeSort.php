<?php


class MergeSort
{
    static function sort(&$arr)
    {
        self::merge_sort_part($arr, 0, count($arr) - 1);
    }

    static function merge_sort_part(&$arr, $p, $r)
    {
        if ($p >= $r) return;

        $q = intval($p / 2 + $r / 2);
        self::merge_sort_part($arr, $p, $q);
        self::merge_sort_part($arr, $q + 1, $r);
        self::merge($arr, $p, $r, $q);
    }

    static function merge(&$arr, $p, $r, $q)
    {
        $tmp = [];
        $i = $p;
        $j = $q + 1;
        $k = $p;
        while ($i <= $q && $j <= $r) {
            if ($arr[$i] < $arr[$j]) {
                $tmp[$k++] = $arr[$i];
                $i++;
            } else {
                $tmp[$k++] = $arr[$j];
                $j++;
            }
        }

        for (; $i <= $q; $i++) {
            $tmp[$k++] = $arr[$i];
        }
        for (; $j <= $r; $j++) {
            $tmp[$k++] = $arr[$j];
        }

        for ($k = $p; $k <= $r; $k++) {
            $arr[$k] = $tmp[$k];
        }
    }
}

$arr = [8, 15, 3, 102, 6, 46, 11];
MergeSort::sort($arr);
echo json_encode($arr);