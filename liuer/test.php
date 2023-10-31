<?php

$a = file_get_contents("000.csv");
$arr = explode("\n", $a);

$min = 1000000;

$data = "";
foreach ($arr as $i => $str) {
    $row = explode(",", $str);
    if (count($row) != 8 || $i == 0) {
        continue;
    }
    $survivalTime = strtotime($row[5]) - strtotime($row[2]);
    $averageAnswerTime = $row[6] / $row[7] / 1000;
    $phone = $row[1] / $min;
    $data .= ip2long($row[0]) / $min . ",$phone,$survivalTime,$averageAnswerTime,0\n";
}

file_put_contents("0.csv", $data);