<?php

class Singleton
{
    private static $instance = null;

    private function __construct()
    {

    }

    private function __clone()
    {

    }

    public static function getInstance(): Singleton
    {
        if (!self::$instance) {
            return new Singleton();
        }
        return self::$instance;
    }

    public function say()
    {
        echo "say" . PHP_EOL;
    }
}

$a = Singleton::getInstance();
$a->say();
