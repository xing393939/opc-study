<?php

$data = "";
foreach (range(10000000, 10005000) as $i => $str) {
    $survivalTime = rand(1, 50);
    $averageAnswerTime = rand(1, 50);
    $phone = rand(13701111330, 18991111330);
    $outcome = rand(0, 1);
    $data .= $str . ",$phone,$survivalTime,$averageAnswerTime,$outcome\n";
}

file_put_contents("0.csv", $data);