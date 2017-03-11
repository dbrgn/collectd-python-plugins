import os.path
import collectd


DEV_REG = '/sys/bus/i2c/devices/i2c-1/new_device'
DEV_REG_PARAM = 'sht21 0x40'
DEV_TMP = '/sys/class/hwmon/hwmon0/temp1_input'
DEV_HUM = '/sys/class/hwmon/hwmon0/humidity1_input'


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

    # Dispatch values
    v_tmp = collectd.Values(type='temperature')
    v_tmp.plugin = 'sht21'
    v_tmp.type = 'temperature'
    v_tmp.dispatch(values=[temperature])
    v_hum = collectd.Values(type='humidity')
    v_hum.plugin = 'sht21'
    v_hum.type = 'humidity'
    v_hum.dispatch(values=[humidity])


collectd.register_init(init)
collectd.register_read(read)
