<?php

$config = [
    ['sentNum' => 0, 'prob' => 0.10],
    ['sentNum' => 0, 'prob' => 0.20],
    ['sentNum' => 0, 'prob' => 0.30],
    ['sentNum' => 0, 'prob' => 0.40],
];

$probArr = [];
foreach ($config as $i => $item) {
    $probArr[$i] = round($item["prob"] * 100);
}

testCase(100, 'getRand');
echo "\n";
testCase(100, 'getFairRand');

function testCase($count, $func)
{
    global $probArr;
    $winArr = [];
    for ($i = 0; $i < $count; $i++) {
        $winIndex = $func($probArr);
        if (isset($winArr[$winIndex])) {
            $winArr[$winIndex]++;
        } else {
            $winArr[$winIndex] = 1;
        }
    }

    for ($i = 0; $i < 4; $i++) {
        echo "item$i sentNum=", $winArr[$i], " prob=", $winArr[$i] / $count, "\n";
    }
}

function getFairRand($probArr)
{
    global $config;
    $sentNum = array_sum(array_column($config, 'sentNum'));
    $waitedArr = [];
    foreach ($config as $i => $item) {
        // 当前是否满足了中奖概率
        if ($sentNum > 0 && $item['sentNum'] / $sentNum < $item['prob']) {
            $waitedArr[$i] = round($item["prob"] * 100);
        }
    }
    if (empty($waitedArr)) {
        $winIndex = getRand($probArr);
    } else {
        $winIndex = getRand($waitedArr);
    }
    $config[$winIndex]['sentNum']++;
    return $winIndex;
}

function getRand($proArr)
{
    $result = -1;
    $proSum = array_sum($proArr);
    if ($proSum < 1) {
        return $result;
    }
    foreach ($proArr as $key => $proCur) {
        $randNum = mt_rand(1, $proSum);
        if ($randNum <= $proCur) {
            $result = $key;
            break;
        } else {
            $proSum -= $proCur;
        }
    }
    return $result;
}
