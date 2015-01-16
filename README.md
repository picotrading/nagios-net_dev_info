net_dev_info.py
===============

This script is a Nagios check which returns information about a particular
network interface.


Usage
-----

```
./net_dev_info.py --warning @2:4 --critical @5: --device eth0 --metric rx_errs
```

To see all options of the plugin, use the following command:

```
./net_dev_info.py --help
```


Testing
-------

Use the following command to test the behaviour for a set of values (sequence of numbers from 0 to 10):

```
$ for N in $(seq 0 10); do ./net_dev_info.py --fake $N; sleep 1; done
```

Which gives output like this:

```
NETDEVINFO OK - rx_errs increased by 0 in 0 seconds | rx_errs=0;@2:4;@5:
NETDEVINFO OK - rx_errs increased by 1 in 1 seconds | rx_errs=1;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 2 in 1 seconds | rx_errs=2;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 3 in 1 seconds | rx_errs=3;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 4 in 1 seconds | rx_errs=4;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 5 in 1 seconds | rx_errs=5;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 6 in 1 seconds | rx_errs=6;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 7 in 1 seconds | rx_errs=7;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 8 in 1 seconds | rx_errs=8;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 9 in 1 seconds | rx_errs=9;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 10 in 1 seconds | rx_errs=10;@2:4;@5:
```

Or use the following command to use randon increments (range from 0 to 5):

```
$ while [ true ]; do ./net_dev_info.py -f $(shuf -i 0-5 -n 1); sleep 1; done
```

Which gives output like this:

```
NETDEVINFO OK - rx_errs increased by 0 in 0 seconds | rx_errs=3;@2:4;@5:
NETDEVINFO OK - rx_errs increased by 0 in 1 seconds | rx_errs=0;@2:4;@5:
NETDEVINFO OK - rx_errs increased by 0 in 1 seconds | rx_errs=0;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 5 in 1 seconds | rx_errs=5;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 5 in 1 seconds | rx_errs=5;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 5 in 1 seconds | rx_errs=5;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 4 in 1 seconds | rx_errs=4;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 3 in 1 seconds | rx_errs=3;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 2 in 1 seconds | rx_errs=2;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 3 in 1 seconds | rx_errs=3;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 4 in 1 seconds | rx_errs=4;@2:4;@5:
NETDEVINFO WARNING - rx_errs increased by 2 in 1 seconds | rx_errs=2;@2:4;@5:
NETDEVINFO OK - rx_errs increased by 0 in 1 seconds | rx_errs=0;@2:4;@5:
NETDEVINFO CRITICAL - rx_errs increased by 5 in 1 seconds | rx_errs=5;@2:4;@5:
```


Requirements
------------

- Python v2.6+
- [`nagiosplugin`](https://pypi.python.org/pypi/nagiosplugin) package


License
-------

MIT


Author
------

Jiri Tyr
