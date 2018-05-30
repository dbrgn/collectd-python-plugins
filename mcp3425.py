# -*- coding: utf-8 -*-
"""
MCP3425 ADC Plugin.

Return supply voltage (in mV) from ADC readings.

This plugin requires the python-smbus package to be installed.

Configure your three voltage divider resistors below.
Default values are 6.8K, 3.6K and 470.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import time

import collectd
import smbus


# I2C address
DEVICE_ADDRESS = 0x68

# Voltage dividers
DIVIDER_R1 = 6800
DIVIDER_R2 = 3600
DIVIDER_R3 = 470

# ADC reference
ADC_REF = 2048  # mV

# Config register bits
BIT_G0 = 0
BIT_G1 = 1
BIT_S0 = 2
BIT_S1 = 3
BIT_OC = 4
BIT_C0 = 5
BIT_C1 = 6
BIT_RDY = 7

# Conversion mode
CONVERSION_MODE_ONESHOT = 0
CONVERSION_MODE_CONT = 1 << BIT_OC

# Sample rate / accuracy
SAMPLE_RATE_240SPS = 0  # 12 bits
SAMPLE_RATE_60SPS = 1 << BIT_S0  # 14 bits
SAMPLE_RATE_15SPS = 1 << BIT_S1  # 16 bits

# PGA gain selection
PGA_GAIN_1 = 0
PGA_GAIN_2 = 1 << BIT_G0
PGA_GAIN_4 = 1 << BIT_G1
PGA_GAIN_8 = (1 << BIT_G1) | (1 << BIT_G0)

# Start a conversion in one shot mode
START_CONVERSION = 1 << BIT_RDY


def get_voltage(measurement, bit):
    """
    Calculate voltage for the specified bit of accuracy.
    """
    v2 = measurement * ADC_REF / (2**bit)
    total_r = DIVIDER_R1 + DIVIDER_R2 + DIVIDER_R3
    return v2 / (DIVIDER_R2 / total_r) * 2


def init():
    collectd.info('mcp3425 plugin: Initialized')


def read():
    # Connect to I2C
    bus = smbus.SMBus(1)

    # Write configuration
    config = START_CONVERSION | CONVERSION_MODE_ONESHOT | SAMPLE_RATE_15SPS | PGA_GAIN_1
    bus.write_byte(DEVICE_ADDRESS, config)

    # Wait a bit for the measurement to finish
    time.sleep(0.15)

    # Read measurement
    data = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 3)
    value = (data[0] << 8) + data[1]

    # Convert to mV
    millivolts = get_voltage(value, 16)

    # Dispatch values
    v_voltage = collectd.Values(plugin='mcp3425', type='voltage', type_instance='supply_voltage')
    v_voltage.dispatch(values=[millivolts])


collectd.register_init(init)
collectd.register_read(read)
