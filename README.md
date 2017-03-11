# Collectd Python Plugins

This is a collections of Python plugin for Collectd.

- `cpu_temp.py`: Report the CPU temperature. Tested on a Raspberry Pi 3.
- `sht21.py`: Measure temperature and relative humidity from a Sensirion SHT21
  sensor connected via I²C. Tested on a Raspberry Pi 3.

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

## License

MIT License, see LICENSE file.
