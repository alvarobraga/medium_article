#ifndef ADC_H_
#define ADC_H_

#include <stdio.h>
#include <stdint.h>
#include "stm32f4xx.h"

#define TCIF0 (1U << 5)  /*Reference Manual, page 188: DMA - Mask to read Transfer Complete \
                             Interrupt Flag*/
#define CTCIF0 (1U << 5) /*Reference Manual, page 189: DMA - Mask to clear interrupt flag - \
                         bit CTCIF6 of the DMA High Interrupt Flag Clear Register (DMA_HIFCR)*/

void pa1_adc_init(void);                                          // Initialise ADC
void start_conversion(void);                                      // Trigger new conversion
void dma2_stream0_init(uint32_t src, uint32_t dst, uint32_t len); // Initialise DMA controller

#endif /* ADC_H_ */