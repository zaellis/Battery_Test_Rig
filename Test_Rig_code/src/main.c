/**
  ******************************************************************************
  * @file    main.c
  * @author  Zachary Ellis
  * @version V1.0
  * @date    3/22/21
  * @brief   Main function for Battery Test Rig
  ******************************************************************************
*/


#include "stm32l4xx.h"

struct ADC_Samples_t{
	int discharge_curr;
	int charge_curr;
	int dut_volt;
};
			

void init_DAC(void) {
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;
	GPIOA->MODER |= GPIO_MODER_MODER4; //Enable PA4 for alternate function (DAC1)
	GPIOA->MODER |= GPIO_MODER_MODER5; //Enable PA5 for alternate function (DAC2)
	RCC->APB1ENR1 |= RCC_APB1ENR1_DAC1EN;
	DAC->CR |= DAC_CR_TSEL1; //software trigger selection
	DAC->CR |= DAC_CR_TEN1;  //enable DAC trigger
	DAC->CR |= DAC_CR_EN1;   //enable DAC
	DAC->CR |= DAC_CR_TSEL2;
	DAC->CR |= DAC_CR_TEN2;
	DAC->CR |= DAC_CR_EN2;
}

void init_ADC(void) {
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOAEN;
	GPIOA->MODER |= GPIO_MODER_MODER0 | GPIO_MODER_MODER1; //Enable PA0, PA1 for ADC
	RCC->AHB2ENR |= RCC_AHB2ENR_GPIOBEN;
	GPIOB->MODER |= GPIO_MODER_MODER0;
	RCC->AHB2ENR |= RCC_AHB2ENR_ADCEN; //Enable PB0 for ADC
	ADC1 ->SQR1 |= ADC_SQR1_L_0 | ADC_SQR1_L_1; //three channels in sequence
	ADC1 ->SQR1 |= ADC_SQR1_SQ1_0 | ADC_SQR1_SQ1_2; //ADC1_IN5
	ADC1 ->SQR1 |= ADC_SQR1_SQ2_1 | ADC_SQR1_SQ2_2; //ADC1_IN6
	ADC1 ->SQR1 |= ADC_SQR1_SQ3_0 | ADC_SQR1_SQ3_1 | ADC_SQR1_SQ3_2 | ADC_SQR1_SQ3_3; //ADC1_IN15
	ADC1->CR |= ADC_CR_ADEN;            //enable ADC
	while(!(ADC1->ISR & ADC_ISR_ADRDY));//wait for ADC to be ready
}

struct ADC_Samples_t get_ADC_samples(void){
	volatile struct ADC_Samples_t samples; //don't know if volatile is needed here but we are writing the struct in a weird way
	int* place;
	place = (void*)&samples;  //address to store sample
	while(!(ADC1->ISR & ADC_ISR_ADRDY)); //wait for ADC to be ready
	ADC1->CR |= ADC_CR_ADSTART;          //start conversion
	for(int i=0; i < sizeof(samples) / sizeof(int); i++){
		while(!(ADC1->ISR & ADC_ISR_EOC));
		*place = ADC1->DR;           //store sample in the value at the address
		place = place + sizeof(int); //increment the address
	}
	ADC1->CR |= ADC_CR_ADSTP; //stop any ongoing conversions. probably don't need this but whatevs
	while(ADC1->CR & ADC_CR_ADSTART); //make sure things actually stop
	return samples;
}

int main(void)
{
	init_DAC();
	init_ADC();
	struct ADC_Samples_t samples;
	for(;;){
		samples = get_ADC_samples();
		samples.charge_curr++;
		samples.charge_curr--;
	}
}
