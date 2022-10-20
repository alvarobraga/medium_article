#include <stdlib.h>
#include <stdint.h>
#include "stm32f4xx.h"
#include "adc.h"
#include "uart.h"
#include "timer.h"
#include "constants.h"

#define DATA 0x20000000 // Define initial address for samples[1000]

typedef struct
{
    uint32_t samples[SAMPLING_SIZE]; // Array that will receive ADC conversion via DMA
    float rms_squared;               // Receives the value of the rms_squared
} Data_t;

#define Data ((Data_t *)DATA) // Declare struct with initial address at 0x20000000

static void dma_callback(void);
static void timer2_callback(void);

int main()
{
    pa1_adc_init();
    uart2_tx_init();
    timer2_1000hz_interrupt_init();
    dma2_stream0_init((uint32_t)&ADC1->DR, (uint32_t)Data->samples, (SAMPLING_SIZE));

    while (1)
        ;
}

static void dma_callback(void)
{
    int n = 0;
    for (n; n < SAMPLING_SIZE; n++)
        printf("%d,\n\r", Data->samples[n]);

    while (1)
        ;
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
    start_conversion(); // Trigger new conversion
}

void TIM2_IRQHandler(void)
{
    // Clear Update Interrupt Flag
    TIM2->SR &= ~(UIF);

    timer2_callback();
}
