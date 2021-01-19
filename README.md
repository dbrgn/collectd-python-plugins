# Collectd Python Plugins

This is a collections of Python plugin for Collectd.

- `cpu_temp.py`: Report the CPU temperature. Tested on a Raspberry Pi 3.
- `sht21.py`: Measure temperature and relative humidity from a Sensirion SHT21
  sensor connected via I²C. Calculate dew point and absolute humidity. Tested
  on a Raspberry Pi 3.
- `shtc3.py`: Measure temperature and relative humidity from a Sensirion SHTC3
  sensor connected via I²C. Calculate dew point and absolute humidity. Tested
  on a Raspberry Pi 3.
- `mcp3425.py`: Measure voltage using an MCP3425 analog-digital converter.

For more information, please refer to [my
blogpost](https://blog.dbrgn.ch/2017/3/10/write-a-collectd-python-plugin/).

## Configuration

Copy the desired Python files to your target system. Then add the module to
your `collectd.conf`. Make sure to adjust the `ModulePath` value. The following
example assumes the plugins were copied to `/opt/collectd_plugins`.

### cpu_temp

If your CPU temperature cannot be read from
`/sys/class/thermal/thermal_zone0/temp`, make sure to adjust that variable too.

    LoadPlugin python
    <Plugin python>
        ModulePath "/opt/collectd_plugins"
        Import "cpu_temp"
        <Module cpu_temp>
            Path "/sys/class/thermal/thermal_zone0/temp"
        </Module>
    </Plugin>

### sht21

For this plugin to work, the `sht21` kernel module must be loaded:

    echo "sht21" > /etc/modules-load.d/sht21.conf

There are currently no configuration options available.

    LoadPlugin python
    <Plugin python>
        ModulePath "/opt/collectd_plugins"
        Import "sht21"
    </Plugin>

### shtc3

For this plugin to work, the `shtc1` kernel module must be loaded:

    echo "shtc1" > /etc/modules-load.d/shtc1.conf
    modprobe shtc1

Default config:

    LoadPlugin python
    <Plugin python>
        ModulePath "/opt/collectd_plugins"
        Import "shtc3"
    </Plugin>

Optionally, the hwmon device (hwmon0 by default) can be configured:

    LoadPlugin python
    <Plugin python>
        ModulePath "/opt/collectd_plugins"
        Import "shtc3"
        <Module shtc3>
            Hwmon "hwmon2"
        </Module>
    </Plugin>

### mcp3425

The plugin assumes that you're using three voltage divider resistors to bring
the voltage into a measurable range. You can configure them in the Python
script.

This plugin requires the python-smbus package to be installed.

There are currently no configuration options available.

    LoadPlugin python
    <Plugin python>
        ModulePath "/opt/collectd_plugins"
        Import "mcp3425"
    </Plugin>

## Other Plugins

This is my personal collection of plugins. If you also created a Collectd
plugin that's great! I won't accept pull requests for now though since I cannot
test and maintain plugins for which I don't have any matching hardware.

Instead, feel free to create a pull request to add your plugin to the list
below!

<!-- - [`name.py`](link-to-plugin): Description of the plugin -->

- [`arris_modem.py`](https://github.com/jakup/collectd-python-plugins): Report
  the upstream/downstream channels of an Arris DOCSIS3 cable modem.

## License

MIT License, see LICENSE file.
