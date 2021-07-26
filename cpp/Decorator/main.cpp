#include <iostream>
#include "ConcreteComponent.h"
#include "ConcreteDecoratorA.h"
#include "ConcreteDecoratorB.h"
#include "Component.h"
using namespace std;

int main(int argc, char *argv[])
{
	ConcreteComponent * pRealProd = new ConcreteComponent();

	Component * pA = new ConcreteDecoratorA(pRealProd);
	pA->operation();

	Component * pB = new ConcreteDecoratorB(pA);
	pB->operation();
	
	delete pRealProd;
	delete pA;
	delete pB;
	return 0;
}
