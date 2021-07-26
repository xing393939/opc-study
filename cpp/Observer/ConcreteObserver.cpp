///////////////////////////////////////////////////////////
//  ConcreteObserver.cpp
//  Implementation of the Class ConcreteObserver
//  Created on:      07-十月-2014 23:00:09
//  Original author: cl
///////////////////////////////////////////////////////////

#include "ConcreteObserver.h"
#include <iostream>
#include <vector>
#include "Subject.h"
using namespace std;

ConcreteObserver::ConcreteObserver(string name){
	m_objName = name;
}

ConcreteObserver::~ConcreteObserver(){

}

void ConcreteObserver::update(Subject * sub){
	m_obeserverState = sub->getState();
	cout << "update oberserver[" << m_objName << "] state:" << m_obeserverState << endl;
}
