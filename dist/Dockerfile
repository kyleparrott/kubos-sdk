FROM kubostech/build:latest
MAINTAINER kyle@kubos.co

RUN git clone https://github.com/openkosmosorg/kubos-sdk /kubos-sdk

#modules
 
RUN git clone https://github.com/openkosmosorg/cmsis-core                   /usr/lib/yotta_modules/cmsis-core
RUN git clone https://github.com/openkosmosorg/cmsis-core-st                /usr/lib/yotta_modules/cmsis-core-st
RUN git clone https://github.com/openkosmosorg/cmsis-core-stm32f4           /usr/lib/yotta_modules/cmsis-core-stm32f4
RUN git clone https://github.com/openkosmosorg/cmsis-core-stm32f407xg       /usr/lib/yotta_modules/cmsis-core-stm32f407xg
RUN git clone https://github.com/openkosmosorg/libcsp                       /usr/lib/yotta_modules/csp
RUN git clone https://github.com/openkosmosorg/freertos                     /usr/lib/yotta_modules/freertos
RUN git clone https://github.com/openkosmosorg/freertos-config-msp430f5529  /usr/lib/yotta_modules/freertos-config-msp430f5529
RUN git clone https://github.com/openkosmosorg/freertos-config-stm32f4      /usr/lib/yotta_modules/freertos-config-stm32f4
RUN git clone https://github.com/openkosmosorg/kubos-core                   /usr/lib/yotta_modules/kubos-core
RUN git clone https://github.com/openkosmosorg/kubos-hal                    /usr/lib/yotta_modules/kubos-hal
RUN git clone https://github.com/openkosmosorg/kubos-hal-stm32f407vg        /usr/lib/yotta_modules/kubos-hal-stm32f407vg
RUN git clone https://github.com/openkosmosorg/kubos-hal-msp430f5529        /usr/lib/yotta_modules/kubos-hal-msp430f5529
RUN git clone https://github.com/openkosmosorg/kubos-rt                     /usr/lib/yotta_modules/kubos-rt
RUN git clone https://github.com/openkosmosorg/stm32cubef4-stm32f407vg      /usr/lib/yotta_modules/stm32cubef4-stm32f407vg

#targets

RUN git clone https://github.com/openkosmosorg/target-kubos-arm-none-eabi-gcc   /usr/lib/yotta_targets/kubos-arm-none-eabi-gcc
RUN git clone https://github.com/openkosmosorg/target-kubos-gcc                 /usr/lib/yotta_targets/kubos-gcc
RUN git clone https://github.com/openkosmosorg/target-stm32f407-disco-gcc       /usr/lib/yotta_targets/stm32f407-disco-gcc
RUN git clone https://github.com/openkosmosorg/target-msp430f5529-gcc           /usr/lib/yotta_targets/msp430f5529-gcc

