# CPU Temperature Plugin for Collectd

This is a simply Python plugin for Collectd that can read the CPU temperature.
It has been tested on a Raspberry Pi 3.

For more information, please refer to [my
blogpost](https://blog.dbrgn.ch/2017/3/10/write-a-collectd-python-plugin/).

## Configuration

Copy the `cpu_temp.py` file to your target system. Make sure to adjust the
`ModulePath`.

If your CPU temperature cannot be read from
`/sys/class/thermal/thermal_zone0/temp`, make sure to adjust that variable too.

    LoadPlugin python
    <Plugin python>
        ModulePath "/etc/collectd"
        Import "cpu_temp"
        <Module cpu_temp>
            Path "/sys/class/thermal/thermal_zone0/temp"
        </Module>
    </Plugin>

## License

MIT License, see LICENSE file.
