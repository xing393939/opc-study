<?php

$a = file_get_contents("111.csv");
$arr = explode("\n", $a);

$data = "";
foreach ($arr as $i => $str) {
    $row = explode(",", $str);
    if (count($row) != 8 || $i == 0) {
        continue;
    }
    $survivalTime = strtotime($row[5]) - strtotime($row[2]);
    $averageAnswerTime = $row[6] / $row[7] / 1000;
    $data .= ip2long($row[0]) . ",$row[1],$survivalTime,$averageAnswerTime,1\n";
}

file_put_contents("1.csv", $data);