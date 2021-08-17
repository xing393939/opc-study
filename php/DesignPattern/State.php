<?php

class BadGumballMachine
{
    private $state = 'no_quarter';
    private $count = 2;

    function insertQuarter()
    {
        if ($this->state == 'has_quarter') {
            echo "has_quarter already";
        } elseif ($this->state == 'no_quarter') {
            $this->state = 'has_quarter';
            echo "insertQuarter success";
        } elseif ($this->state == 'sold_out') {
            echo 'sold_out';
        } elseif ($this->state == 'sold') {
            echo 'you have one already';
        }
    }

    function ejectQuarter()
    {
        if ($this->state == 'has_quarter') {
            echo "ejectQuarter success";
            $this->state = 'no_quarter';
        } elseif ($this->state == 'no_quarter') {
            echo "no_quarter";
        } elseif ($this->state == 'sold_out') {
            echo 'no_quarter';
        } elseif ($this->state == 'sold') {
            echo 'you have crank already';
        }
    }

    function turnCrank()
    {
        if ($this->state == 'has_quarter') {
            echo "turnCrank success";
            $this->state = 'sold';
        } elseif ($this->state == 'no_quarter') {
            echo "no_quarter";
        } elseif ($this->state == 'sold_out') {
            echo 'sold_out';
        } elseif ($this->state == 'sold') {
            echo 'you have crank already';
        }
    }

    function dispense()
    {
        if ($this->state == 'has_quarter') {
            echo "nothing";
        } elseif ($this->state == 'no_quarter') {
            echo "nothing";
        } elseif ($this->state == 'sold_out') {
            echo 'nothing';
        } elseif ($this->state == 'sold') {
            $this->count--;
            if ($this->count < 0) {
                echo 'sold_out';
                $this->state = 'sold_out';
            } else {
                echo 'dispense success';
                $this->state = 'no_quarter';
            }
        }
    }
}

class has_quarter
{
    private $machine = null;

    public function __construct(GoodGumballMachine $machine)
    {
        $this->machine = $machine;
    }

    function insertQuarter()
    {
        echo 'has_quarter already';
    }

    function ejectQuarter()
    {
        echo 'ejectQuarter success';
        $this->machine->setState('no_quarter');
    }

    function turnCrank()
    {
        echo 'turnCrank success';
        $this->machine->setState('sold');
    }

    function dispense()
    {
        echo 'nothing';
    }
}

class no_quarter
{
    private $machine = null;

    public function __construct(GoodGumballMachine $machine)
    {
        $this->machine = $machine;
    }

    function insertQuarter()
    {
        echo 'insertQuarter success';
        $this->machine->setState('has_quarter');
    }

    function ejectQuarter()
    {
        echo 'no_quarter';
    }

    function turnCrank()
    {
        echo 'nothing';
    }

    function dispense()
    {
        echo 'nothing';
    }
}

class sold_out
{
    private $machine = null;

    public function __construct(GoodGumballMachine $machine)
    {
        $this->machine = $machine;
    }

    function insertQuarter()
    {
        echo 'sold_out';
    }

    function ejectQuarter()
    {
        echo 'sold_out';
    }

    function turnCrank()
    {
        echo 'sold_out';
    }

    function dispense()
    {
        echo 'sold_out';
    }
}

class sold
{
    private $machine = null;

    public function __construct(GoodGumballMachine $machine)
    {
        $this->machine = $machine;
    }

    function insertQuarter()
    {
        echo 'nothing';
    }

    function ejectQuarter()
    {
        echo 'no_quarter';
    }

    function turnCrank()
    {
        echo 'nothing';
    }

    function dispense()
    {
        $this->machine->count--;
        if ($this->machine->count < 0) {
            echo 'sold_out';
            $this->machine->setState('sold_out');
        } else {
            echo 'dispense success';
            $this->machine->setState('no_quarter');
        }
    }
}

class GoodGumballMachine
{
    private $stateArr = [];
    private $state = null;
    public $count = 2;

    public function __construct()
    {
        $this->stateArr = [
            'has_quarter' => new has_quarter($this),
            'no_quarter' => new no_quarter($this),
            'sold_out' => new sold_out($this),
            'sold' => new sold($this),
        ];
        $this->setState('no_quarter');
    }

    function setState($name)
    {
        $this->state = $this->stateArr[$name];
    }

    function insertQuarter()
    {
        $this->state->insertQuarter();
    }

    function ejectQuarter()
    {
        $this->state->ejectQuarter();
    }

    function turnCrank()
    {
        $this->state->turnCrank();
    }

    function dispense()
    {
        $this->state->dispense();
    }
}

$bad = new BadGumballMachine();
$bad->insertQuarter();
$bad->turnCrank();
$bad->dispense();
echo "\n";
$bad->insertQuarter();
$bad->turnCrank();
$bad->dispense();
echo "\n";
$bad->insertQuarter();
$bad->turnCrank();
$bad->dispense();
echo "\n";
$bad->insertQuarter();
$bad->turnCrank();
echo "\n";

$good = new GoodGumballMachine();
$good->insertQuarter();
$good->turnCrank();
$good->dispense();
echo "\n";
$good->insertQuarter();
$good->turnCrank();
$good->dispense();
echo "\n";
$good->insertQuarter();
$good->turnCrank();
$good->dispense();
echo "\n";
$good->insertQuarter();
$good->turnCrank();
echo "\n";