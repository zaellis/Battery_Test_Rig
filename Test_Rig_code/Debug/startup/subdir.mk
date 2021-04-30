################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
S_SRCS += \
../startup/startup_stm32.s 

OBJS += \
./startup/startup_stm32.o 


# Each subdirectory must supply rules for building sources it contributes
startup/%.o: ../startup/%.s
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Assembler'
	@echo $(PWD)
	arm-none-eabi-as -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Device/ST/STM32L4xx/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/device" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Core/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/core" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc" -g -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


