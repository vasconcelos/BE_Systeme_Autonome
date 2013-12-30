/***************************************************************
 * BE système autonome           							   *
 * Created by Joao VASCONCELOS	 							   *
 * Date: 12/12/2013				 							   *
 *								 							   *
 * File: Init_System.c			 							   *
 * Description: This file contains all system configurations   *
 ***************************************************************/


/***************************************************************
 *
 * INCLUDE FILES
 *
 ***************************************************************/
#include <Init_System.h>

/***************************************************************
 *
 * FUNCTIONS
 *
 ***************************************************************/

void init_System(void)
{
	// Config for system clock (8MHz by internal clock)
	OSCTUNE = 0x00;//0xC0;
	OSCCON = 0x77; 		  // Use internal clock as clock system

	// Enable periodic interruption timeout + enable maskable interrupt 
	T0CON = 0xD8;          //timeout 8bits (8M/4*256 = 7812.5Hz)
	INTCONbits.TMR0IE = 1;
	INTCONbits.GIEH = 1;
	
	// Config Input pins for all IR sensors
	TRISBbits.TRISB7 = 1;
	TRISBbits.TRISB6 = 1;
	TRISBbits.TRISB5 = 1;

	// Config Input pin for ultrason sensor
	TRISBbits.TRISB4 = 1;
	
	// Ports for USART/UART/serial communication
	TRISCbits.TRISC7 = 0; // RX
	TRISCbits.TRISC6 = 1; // TX

	// Config for Serial comm
	// Ports for development board ICD2 leds for tests
	TRISBbits.TRISB0 = 0;
	PORTB = 0;
}