/***************************************************************
 * BE système autonome           							   *
 * Created by Joao VASCONCELOS	 							   *
 * Date: 12/12/2013				 							   *
 *								 							   *
 * File: System_Manager.c		 							   *
 * Description: This file contains the main application and    *
 *				call back functions							   *
 ***************************************************************/


/***************************************************************
 *
 * INCLUDE FILES
 *
 ***************************************************************/
#include <System_Manager.h>


/***************************************************************
 *
 * DEFINES
 *
 ***************************************************************/
#define TURN_LEFT
#define TURN_RIGTH
#define OBSTACLE
#define KEEP_GOING

/***************************************************************
 *
 * GLOBAL VARIABLES
 *
 ***************************************************************/
unsigned int Led_State = 0;
unsigned char sensor_state = 0x00; // 8 bits
unsigned long i = 0;


/***************************************************************
 *
 * FUNCTIONS
 *
 ***************************************************************/
#pragma interrupt it_routine

void it_routine(void)
{
	if(INTCONbits.TMR0IF)
	{
		INTCONbits.TMR0IF = 0;
		i++;
		if(i == 79) // reading inputs every 10.112 ms
		{
			// Reading Ports
			sensor_state = ((PORTB & 0xF0) >> 4); 
			sendData(sensor_state);
			if(Led_State == 0)
			{
				PORTB |= 0b00000001;
				Led_State = 1;
			}
			else
			{
				PORTB &= 0b11111110;
				Led_State = 0;
			}
		i = 0;
		}
	}
}

#pragma code vecteur_d_IT = 0x08
void it_saut(void)
{
_asm goto it_routine _endasm
}


#pragma code
void sendData(unsigned char data)
{
	if(TXSTAbits.TRMT == 1)
	{
		TXREG = data;
	}
}