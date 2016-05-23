# Kubos SDK

### Installation: 

Install the kubos sdk

```
$ pip install kubos-sdk
```

Pull the latest kubos-sdk docker container

```
$ kubos update
```

### Usage: 

#### Create a new KubOS project:
 
```
$ kubos init  <project name> 
```

 
#### Set target device: 
 
```
$ kubos target <target> 
```
The current supported targets are: 

STM32F407 Discovery Board - `stm32f407-disco-gcc@openkosmosorg/target-stm32f407-disco-gcc`

MSP430F5529 Launchpad - `msp430f5529-gcc@openkosmosorg/target-msp430f5529-gcc`

#### Build your project

```
$ kubos build
$ kubos build -v #for verbose builds
```

#### Flash your target device

```
$ kubos flash
```