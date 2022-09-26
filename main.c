#include <stdlib.h>
#include <stdint.h>
#include "stm32f4xx.h"
#include "adc.h"
#include "uart.h"
//#include "uart6.h"
#include "timer.h"
#include "constants.h"

#define DATA	0x20000000   //Define initial address for samples[1000]
#define GAIN  0x3F800000;  //1.

typedef struct
{
	uint32_t samples[SAMPLING_SIZE]; //Array that will receive ADC conversion via DMA
	uint32_t dummy[1];               //Inserts a 4-byte separation between samples[1000] and variance to avoid overlapping
	float variance;                  //Receives the value of the variance calculated in the function Filter
	uint32_t dummy2[1];
	uint32_t gain;
} Data_t;


#define Data ((Data_t*) DATA) //Declare struct with initial address at 0x20000000

extern void Filter(uint32_t * sampling_vector, float * variance, uint32_t * gain); //Function that implements the Butterworth filter and calculates variance
extern inline void __reallocate_stack(void);

static void dma_callback(void);
static void timer2_callback(void);


int main()
{	
	__reallocate_stack();
	pa1_adc_init();
  uart2_tx_init();
	timer2_1000hz_interrupt_init();
	dma2_stream0_init((uint32_t)&ADC1->DR, (uint32_t)Data->samples, (SAMPLING_SIZE));	
	
	while(1)
		;
}

static void dma_callback(void)
{
	Filter(Data->samples,&Data->variance, &Data->gain);
	printf("%.4f\n\r", Data->variance);
}

void DMA2_Stream0_IRQHandler(void)
{
	/*Check for transfer complete interrupt*/
	if (DMA2->LISR & TCIF0)
	{
		/*Clear flag*/
		DMA2->LIFCR |= CTCIF0;

		dma_callback();
	}
}

static void timer2_callback(void)
{
	start_conversion();
}

void TIM2_IRQHandler(void)
{
	// Clear Update Interrupt Flag
	TIM2->SR &= ~(UIF);

	timer2_callback();
}

