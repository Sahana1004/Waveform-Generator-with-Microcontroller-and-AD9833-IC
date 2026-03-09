# Waveform Generator using Microcontroller and AD9833 IC

## Overview

This project implements a programmable waveform generator using the **AD9833 Direct Digital Synthesis (DDS) IC** controlled by an **Arduino Nano**. The system is capable of generating different waveforms such as **sine, square, and triangle waves** with adjustable frequency. Communication between the microcontroller and the AD9833 is established through the **SPI (Serial Peripheral Interface)** protocol.

## Features

* Generation of **sine, square, and triangle waveforms**
* **Adjustable output frequency**
* SPI communication between Arduino Nano and AD9833
* Compact and low-cost signal generation system
* Suitable for laboratory testing and embedded electronics experiments

## Hardware Components

* Arduino Nano (Microcontroller)
* AD9833 DDS Waveform Generator IC
* Resistors and passive components
* Power supply
* Breadboard / PCB connections

## Software

* Arduino IDE
* Embedded C / Arduino code for SPI communication and waveform control

## Working Principle

The AD9833 IC generates waveforms using **Direct Digital Synthesis (DDS)**. The Arduino Nano sends configuration commands to the AD9833 through the SPI interface. These commands control parameters such as waveform type and frequency. Based on the configuration, the AD9833 produces the required analog waveform at its output.

## Applications

* Signal generation for electronics experiments
* Testing and debugging analog circuits
* Educational demonstrations of DDS-based waveform generation
* Embedded systems and communication system experiments

## Project Structure

```
Waveform-Generator-with-Microcontroller-and-AD9833-IC
│
├── code/            # Arduino code for waveform generation
├── circuit/         # Circuit diagrams or schematics
├── images/          # Setup images or output waveform screenshots
└── README.md        # Project documentation
```


