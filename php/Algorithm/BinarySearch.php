<?php


class BinarySearch
{
    static function search($arr, $dist)
    {
        $low = 0;
        $high = count($arr) - 1;
        while ($low <= $high) {
            $mid = intval(($low + $high) / 2);
            if ($arr[$mid] == $dist) {
                return $mid;
            } elseif ($arr[$mid] > $dist) {
                $high = $mid - 1;
            } else {
                $low = $mid + 1;
            }
        }
        return -1;
    }

    static function searchFirstOne($arr, $dist)
    {
        $low = 0;
        $high = count($arr) - 1;
        while ($low <= $high) {
            $mid = intval(($low + $high) / 2);
            if ($arr[$mid] == $dist) {
                for ($i = $mid - 1; $i >= 0; $i --) {
                    if ($arr[$i] == $dist) {
                        $mid = $i;
                    }
                }
                return $mid;
            } elseif ($arr[$mid] > $dist) {
                $high = $mid - 1;
            } else {
                $low = $mid + 1;
            }
        }
        return -1;
    }
}

$arr = [1, 3, 4, 5, 6, 8, 8, 8, 11, 18];
var_dump(BinarySearch::search($arr, 8));
var_dump(BinarySearch::searchFirstOne($arr, 8));