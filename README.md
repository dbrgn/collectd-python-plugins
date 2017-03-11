# Collectd Python Plugins

This is a collections of Python plugin for Collectd.

- `cpu_temp`: Report the CPU temperature. Tested on a Raspberry Pi 3.

For more information, please refer to [my
blogpost](https://blog.dbrgn.ch/2017/3/10/write-a-collectd-python-plugin/).

## Configuration

Copy the desired Python files to your target system. Make sure to adjust the
`ModulePath`. The following example assumes they were copied to
`/opt/collectd_plugins`.

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

## License

MIT License, see LICENSE file.
