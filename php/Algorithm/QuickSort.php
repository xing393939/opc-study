<?php


class QuickSort
{
    static function sort(&$arr)
    {
        self::quick_sort_part($arr, 0, count($arr) - 1);
    }

    static function quick_sort_part(&$arr, $p, $r)
    {
        if ($p >= $r) return;

        $q = self::partition($arr, $p, $r);
        self::quick_sort_part($arr, $p, $q);
        self::quick_sort_part($arr, $q + 1, $r);
    }

    static function partition(&$arr, $p, $r)
    {
        $q = $p;
        $value = $arr[$q];
        for ($i = $p + 1; $i <= $r; $i++) {
            if ($value > $arr[$i]) {
                $arr[$q] = $arr[$i];
                $q++;
                $arr[$i] = $arr[$q];
            }
        }
        $arr[$q] = $value;
        return $q;
    }
}

$arr = [8, 15, 3, 102, 6, 46, 11, 2, 59];
QuickSort::sort($arr);
echo json_encode($arr);