<?php

$a = file_get_contents("000.csv");
$arr = explode("\n", $a);

$data = "";
foreach ($arr as $i => $str) {
    $row = explode(",", $str);
    if (count($row) != 8 || $i == 0) {
        continue;
    }
    $survivalTime = strtotime($row[5]) - strtotime($row[2]);
    $averageAnswerTime = $row[6] / $row[7] / 1000;
    $ip = substr($row[1], 0, 5);
    $data .= str_replace('.', ',', $row[0]) . ",$ip,$survivalTime,$averageAnswerTime,0\n";
}

file_put_contents("0.csv", $data);