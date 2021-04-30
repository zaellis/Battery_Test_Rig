################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../src/main.c \
../src/stm32l4xx_it.c \
../src/syscalls.c \
../src/system_stm32l4xx.c 

OBJS += \
./src/main.o \
./src/stm32l4xx_it.o \
./src/syscalls.o \
./src/system_stm32l4xx.o 

C_DEPS += \
./src/main.d \
./src/stm32l4xx_it.d \
./src/syscalls.d \
./src/system_stm32l4xx.d 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.c
	@echo 'Building file: $<'
	@echo 'Invoking: MCU GCC Compiler'
	@echo $(PWD)
	arm-none-eabi-gcc -mcpu=cortex-m4 -mthumb -mfloat-abi=hard -mfpu=fpv4-sp-d16 -DSTM32 -DSTM32L4 -DSTM32L432KCUx -DDEBUG -DSTM32L432xx -DUSE_HAL_DRIVER -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/STM32L4xx_HAL_Driver/Inc/Legacy" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Device/ST/STM32L4xx/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/device" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Core/Inc" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/Dev_Test/Drivers/CMSIS/Include" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/CMSIS/core" -I"E:/Documents/Github/Battery_Test_Rig/Test_Rig_code/HAL_Driver/Inc" -O0 -g3 -Wall -fmessage-length=0 -ffunction-sections -c -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


