/***************************************************************
 * BE système autonome           							   *
 * Created by Joao VASCONCELOS	 							   *
 * Date: 12/12/2013				 							   *
 *								 							   *
 * File: System_Manager.c		 							   *
 * Description: This file contains the main application and    *
 *				call back functions							   *
 ***************************************************************/


#ifndef _SYSTEM_MANAGER_H_
#define _SYSTEM_MANAGER_H_

/***************************************************************
 *
 * INCLUDE FILES
 *
 ***************************************************************/
#include <p18f2580.h>


/***************************************************************
 *
 * PROTOTYPES
 *
 ***************************************************************/
 void it_routine(void);
 void sendData(unsigned char data);

#endif//_SYSTEM_MANAGER_H_