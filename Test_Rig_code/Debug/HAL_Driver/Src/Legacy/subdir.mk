################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../HAL_Driver/Src/Legacy/stm32l4xx_hal_can.c 

OBJS += \
./HAL_Driver/Src/Legacy/stm32l4xx_hal_can.o 

C_DEPS += \
./HAL_Driver/Src/Legacy/stm32l4xx_hal_can.d 


# Each subdirectory must supply rules for building sources it contributes
HAL_Driver/Src/Legacy/%.o: ../HAL_Driver/Src/Legacy/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DSTM32 -DSTM32L4 -DSTM32L432KCUx -DDEBUG -DSTM32L432xx -DUSE_HAL_DRIVER -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Device/ST/STM32L4xx/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/device" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Core/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/core" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc" -O0 -g3 -Wall -fmessage-length=0 -ffunction-sections -c -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


