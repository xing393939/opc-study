<?php

class Receiver
{
    public function action()
    {
        echo 'action...' . PHP_EOL;
    }
}

abstract class Command
{
    protected $receiver;

    public function __construct(Receiver $receiver)
    {
        $this->receiver = $receiver;
    }

    public function execute()
    {

    }
}

class ConcreteCommand extends Command
{
    public function execute()
    {
        $this->receiver->action();
    }
}

class Invoker
{
    private $command;

    public function __construct(Command $command)
    {
        $this->command = $command;
    }

    public function call()
    {
        $this->command->execute();
    }
}

$receiver = new Receiver();
$command = new ConcreteCommand($receiver);
$invoker = new Invoker($command);

$invoker->call();