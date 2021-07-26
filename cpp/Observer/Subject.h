///////////////////////////////////////////////////////////
//  Subject.h
//  Implementation of the Class Subject
//  Created on:      07-十月-2014 23:00:10
//  Original author: cl
///////////////////////////////////////////////////////////

#if !defined(EA_61998456_1B61_49f4_B3EA_9D28EEBC9649__INCLUDED_)
#define EA_61998456_1B61_49f4_B3EA_9D28EEBC9649__INCLUDED_

#include "Observer.h"
#include <vector>
using namespace std;

class Subject
{

public:
	Subject();
	virtual ~Subject();
	Observer *m_Obeserver;

	void attach(Observer * pObeserver);
	void detach(Observer * pObeserver);
	void notify();
		
	virtual int getState() = 0;
	virtual void setState(int i)= 0;
	
private:
	vector<Observer*> m_vtObj;

};
#endif // !defined(EA_61998456_1B61_49f4_B3EA_9D28EEBC9649__INCLUDED_)
