# -*- coding: utf-8 -*-
"""
SHT21 Sensor Plugin.

Return temperature and relative humidity from sensor readings.

Calculcate and return absolute humidity and dew point.

Source for calculations:
http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import os.path
import math

import collectd


DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
DEV_REG_PARAM = 'sht21 0x40'
DEV_TMP = '/sys/class/hwmon/hwmon0/temp1_input'
DEV_HUM = '/sys/class/hwmon/hwmon0/humidity1_input'


def pws_constants(t):
    """
    Lookup-table for water vapor saturation pressure constants (A, m, Tn).
    """
    if t < -20:
        raise ValueError('Temperature out of range (-20 - 350°C')
    if t < 50:
        return (6.116441, 7.591386, 240.7263)
    if t < 100:
        return (6.004918, 7.337936, 229.3975)
    if t < 150:
        return (5.856548, 7.27731, 225.1033)
    if t < 200:
        return (6.002859, 7.290361, 227.1704)
    return (9.980622, 7.388931, 263.1239)


def pws(t):
    r"""
    Calculate water vapor saturation pressure based on temperature (in hPa).

        P_{WS} = A \cdot 10^{\frac{m \cdot T}{T + T_n}}

    """
    A, m, Tn = pws_constants(t)
    power = (m * t) / (t + Tn)
    return A * 10 ** power


def pw(t, rh):
    r"""
    Calculate Pw (in hPa).

        P_W = P_{WS} \cdot RH / 100

    """
    return pws(t) * rh / 100


def td(t, rh):
    r"""
    Calculate the dew point (in °C).

        T_d = \frac{T_n}{\frac{m}{log_{10}\left(\frac{P_w}{A}\right)} - 1}

    """
    A, m, Tn = pws_constants(t)
    Pw = pw(t, rh)
    return Tn / ((m / math.log(Pw / A, 10)) - 1)


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def ah(t, rh):
    r"""
    Calculate the absolute humidity (in g/m³).

        A = C \cdot P_w / T

    """
    C = 2.16679
    Pw = pw(t, rh)
    T = celsius_to_kelvin(t)
    return C * (Pw * 100) / T


def init():
    if os.path.isfile(DEV_TMP) and os.path.isfile(DEV_HUM):
        collectd.info('sht21 plugin: Sensor already registered in sysfs')
    else:
        with open(DEV_REG, 'wb') as f:
            f.write(DEV_REG_PARAM)
        collectd.info('sht21 plugin: Sensor successfully registered in sysfs')


def read():
    # Read values
    with open(DEV_TMP, 'rb') as f:
        val = f.read().strip()
        temperature = float(int(val)) / 1000
    with open(DEV_HUM, 'rb') as f:
        val = f.read().strip()
        humidity = float(int(val)) / 1000

    # Calculate values
    try:
        dewpoint = td(temperature, humidity)
    except ValueError as e:
        collectd.error('sht21 plugin: Could not calculate dew point: %s' % e)
        dewpoint = 0
    absolute_humidity = ah(temperature, humidity)

    # Dispatch values
    v_tmp = collectd.Values(plugin='sht21', type='temperature', type_instance='current')
    v_tmp.dispatch(values=[temperature])
    v_hum = collectd.Values(plugin='sht21', type='humidity', type_instance='relative_humidity')
    v_hum.dispatch(values=[humidity])
    v_abs = collectd.Values(plugin='sht21', type='gauge', type_instance='absolute_humidity')
    v_abs.dispatch(values=[absolute_humidity])
    v_dew = collectd.Values(plugin='sht21', type='temperature', type_instance='dewpoint')
    v_dew.dispatch(values=[dewpoint])


collectd.register_init(init)
collectd.register_read(read)
