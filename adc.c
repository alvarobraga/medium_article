#include "adc.h"

/**** DMA *****/
#define DMA2EN (1U << 22)		  /*Reference Manual, page 117: Mask to enable clock access \
									to DMA module 2*/
#define DMA_STREAM_EN (1U << 0)	  /*Reference Manual, page 190: Mask to enable DMA stream - bit EN of the \
									DMA stream X configuration register (DMA_SxCR)*/
#define CHSEL0 (0xF1FFFFFF)		  /*Reference Manual, page 190: Mask to select channel 0   \
									DMA - DMA Stream X Configuration Register (DMA_SxCR) - \
									refer also to page 170*/
#define MINC (1U << 10)			  /*Reference Manual, page 190: Mask to tell the DMA_SxCR register to \
									increment the memory address pointer after each data transfer*/
#define PERIPH_2_MEM (0xFFFFFF3F) /*Reference Manual, page 190: Mask to tell the DMA_SxCR register \
									the direction of data transfer, which in the case of this      \
									project is from peripheral to memory*/
#define TCIE (1U << 4)			  /*Reference Manual, page 190: Mask to enable Transfer Complete \
									interrupt*/
#define DMA (1U << 8)			  /*Reference Manual, page 231: Mask to enable DMA for single conversion \
									bit DMA of ADC_CR2 (ADC Control Register 2)*/
#define DDS (1U << 9)			  /*Reference Manual, page 231: Mask to enable continuous acceptance \
									of DMA requests*/
#define CIRC (1U << 8)			  /*Reference Manual, page 190: Mask to enable DMA Circular Mode*/

#define PSIZE (1U << 12) /*Reference Manual, page 190: Mask to configure the peripheral     \
						   data size as word. Unless we're using FIFO mode,                 \
						   the width of the data for the source and destination must match. \
						   Since in the function dma2_stream0_init both source and          \
						   destination are cast into uint32_t, PSIZE is of size word*/

#define MSIZE (1U << 14) /*Reference Manual, page 190: Mask to configure the memory         \
						   data size as word. Unless we're using FIFO mode,                 \
						   the width of the data for the source and destination must match. \
						   Since in the function dma2_stream0_init both source and          \
						   destination are cast into uint32_t, MSIZE is of size word*/

/**** ADC *****/
#define GPIOAEN (1U << 0)  // Reference Manual pg. 117 - Mask to enable clock access to Port A
#define ADC1EN (1U << 8)   // Reference Manual pg. 121 - mask to enable clock access to ADC
#define AS_ANALOG (0xC)	   /*Reference manual pg. 157 - Mask to Set port PA1 in \
								  analog mode in the MODER register*/
#define ADC_CH1 (1U << 0)  // Reference manual pg. 236 - Mask to program SQ3 as channel 1
#define ADC_SEQ_LEN (0x0)  // Reference Manual pg. 235 - Mask to set conversion length to 1.
#define ADON (1U << 0)	   // Reference Manual pg. 233 - Mask to enable ADC module.
#define SWSTART (1U << 30) // Reference Manual pg. 231 - Mask to trigger conversion via software.
#define EOC (1U << 1)	   /*Reference Manual pg. 228 - Mask to check status of the conversion \
														(finished or not finished)*/

void dma2_stream0_init(uint32_t src, uint32_t dst, uint32_t len)
{
	/*Enable clock access to DMA2*/
	RCC->AHB1ENR |= DMA2EN;

	/*Disable DMA2 Stream0 - this is necessary to allow the software to program the configuration*/
	DMA2_Stream0->CR &= ~DMA_STREAM_EN;

	/*Wait until DMA2 Stream0 is disabled*/
	while (DMA2_Stream0->CR & DMA_STREAM_EN)
		;

	/*Clear all interrupt flags of Stream0 - Reference Manual, page 189: DMA Low Interrupt Flag
	  Clear Register - LIFCR clear interrupts from streams 0 to 3*/
	DMA2->LIFCR |= (1U << 0);
	DMA2->LIFCR |= (1U << 2);
	DMA2->LIFCR |= (1U << 3);
	DMA2->LIFCR |= (1U << 4);
	DMA2->LIFCR |= (1U << 5);

	/*Set the source buffer - Reference Manual, page 194: DMA Stream X Peripheral Address
	  Register - in this project, we're sending from ADC to the memory (Peripheral to Memory).
	  For this reason, the source address is of a peripheral.*/
	DMA2_Stream0->PAR = src;

	/*Set the destination buffer - Reference Manual, page 194: DMA Stream X memory 0 address register -
	  in this project, we're sending from ADC to the memory (Peripheral to Memory).
	  For this reason, the destination address is of a memory.*/
	DMA2_Stream0->M0AR = dst;

	/*Set the length - Reference Manual, page 193: DMA Stream X number of Data Register - a 16-bit
	  register that receives the number of items to be transferred (0 up to 65535)*/
	DMA2_Stream0->NDTR = len;

	/*Select DMA stream and channel*/
	DMA2_Stream0->CR &= CHSEL0;

	/*Enable memory increment*/
	DMA2_Stream0->CR |= MINC;

	/*Configure the transfer direction*/
	DMA2_Stream0->CR &= PERIPH_2_MEM;

	/*Enable Transfer Complete Interrupt*/
	DMA2_Stream0->CR |= TCIE;

	/*Enable DMA Circular Mode*/
	DMA2_Stream0->CR |= CIRC;

	/*Informs the DMA that the peripheral data size is 32-bits*/
	DMA2_Stream0->CR |= PSIZE;

	/*Informs the DMA that the memory data size is 32-bits*/
	DMA2_Stream0->CR |= MSIZE;

	/*Enable direct mode and disable FIFO - Reference Manual, page 195: DMA Stream X FIFO Control
	  Register (DMA_SxFCR)*/
	DMA2_Stream0->FCR = 0;

	/*Enable DMA2 Stream0*/
	DMA2_Stream0->CR |= DMA_STREAM_EN;

	/*Enable DMA interrupt*/
	NVIC_EnableIRQ(DMA2_Stream0_IRQn);
}

void pa1_adc_init(void)
{
	/***Configure the ADC pin***/

	/*Enable clock access to GPIOA - data sheet, page 40*/
	RCC->AHB1ENR |= GPIOAEN;

	/*Set the mode of PA1 and PA4 to analog - Reference Manual, page 157*/
	GPIOA->MODER |= AS_ANALOG;

	/***Configure the ADC module - Reference Manual, page 121***/
	/*Enable clock access to the ADC module*/
	RCC->APB2ENR |= ADC1EN;

	/*Conversion sequence start*/
	ADC1->SQR3 = ADC_CH1;

	/*Conversion sequence length - Reference Manual page 235*/
	ADC1->SQR1 = ADC_SEQ_LEN;

	/*Enable ADC1 DMA*/
	ADC1->CR2 |= DMA;

	/*Enable continue accept DMA requests*/
	ADC1->CR2 |= DDS;

	/*Enable the ADC module*/
	ADC1->CR2 |= ADON;
}

void start_conversion(void)
{
	/*Start ADC conversion*/
	ADC1->CR2 |= SWSTART;
}