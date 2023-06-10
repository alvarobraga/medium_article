#include <stdlib.h>
#include <stdint.h>
#include "stm32f4xx.h"
#include "adc.h"
#include "uart.h"
//#include "uart6.h"
#include "timer.h"

#define DATA 0x20000000 // Define initial address for samples[2000]
#define GAIN  0x3F800000  //1

typedef struct
{
    uint32_t samples[SAMPLING_SIZE]; // Array that will receive ADC conversion via DMA
    float rms_squared;               // Receives the value of the variance calculated in the function Filter
    uint32_t gain;
    uint32_t copy_of_samples[SAMPLING_SIZE];
} Data_t;

typedef union
{
    uint32_t priority_timer2;
    uint32_t priority_dma;
} Priority_t;

#define Data ((Data_t *)DATA) // Declare struct with initial address at 0x20000000

extern void Filter(uint32_t *sampling_vector, float *rms_squared, uint32_t *gain); // Function that implements the Butterworth filter and calculates rms_squared
extern inline void __relocate_stack(void);

static void dma_callback(void);
static void timer2_callback(void);


int main()
{
    __relocate_stack();
    pa1_adc_init();
    uart2_tx_init();
    timer2_1000hz_interrupt_init();
    dma2_stream0_init((uint32_t)&ADC1->DR, (uint32_t)Data->samples, (SAMPLING_SIZE));
    Data->gain = GAIN;

    NVIC_SetPriorityGrouping(0UL);
    Priority_t priorities;
    priorities.priority_timer2 = NVIC_EncodePriority(0UL, 0, 0);
    NVIC_SetPriority(TIM2_IRQn, priorities.priority_timer2);
    priorities.priority_dma = NVIC_EncodePriority(0UL, 1, 0);
    NVIC_SetPriority(DMA2_Stream0_IRQn, priorities.priority_dma);

    while (1)
        ;
}

static void dma_callback(void)
{
    int i;
    for (i = 0; i < 2000; i++){
        Data->copy_of_samples[i] = Data->samples[i];
		}

    Filter(Data->copy_of_samples, &Data->rms_squared, &Data->gain);
    printf("%.4f\n\r", Data->rms_squared);
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
