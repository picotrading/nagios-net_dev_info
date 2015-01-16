#!/usr/bin/python2


from time import time
from os.path import isfile
import argparse
import logging
import nagiosplugin
import re


_log = logging.getLogger('nagiosplugin')


# Class which allows to share values between the probe and the summary class
class Storage():
    def __init__(self, all_metrics, device, metric, cur_time, tmp):
        self.all_metrics = all_metrics
        self.device = device
        self.metric = metric
        self.cur_time = cur_time
        self.tmp = tmp
        self.prev_time = 0
        self.prev_val = 0


# Class which performs the check
class NetDevInfo(nagiosplugin.Resource):
    def __init__(self, storage, fake=None):
        self.storage = storage
        self.fake = fake

    def probe(self):
        f_io_name = (
            '%s/nagios_net_dev_%s_%s' %
            (self.storage.tmp, self.storage.device, self.storage.metric))

        # Open data file
        f_data = open('/proc/net/dev')

        # Pattern to tokenize the line
        pattern = re.compile("\s+")

        # Line counter
        line_cnt = 0

        # Reference to the storage class
        s = self.storage

        for line in f_data:
            # Skip first two lines
            if line_cnt > 1:
                data = pattern.split(line.lstrip().replace(':', ''))
                device_name = data[0]

                # Get metric only for the specified device
                if device_name == s.device:
                    cur_val = int(data[s.all_metrics.index(s.metric) + 1])

                    if isfile(f_io_name):
                        # Read the last value from the file
                        f_in = open(f_io_name, 'r')
                        line = f_in.read()
                        f_in.close()

                        (s.prev_time, s.prev_val) = map(int, line.split('\t'))
                    else:
                        # First run
                        s.prev_time = s.cur_time
                        s.prev_val = cur_val

                    if self.fake is not None:
                        # Allow to fake the value
                        cur_val = self.fake + s.prev_val
                    elif s.prev_val > cur_val:
                        # When the counter was reseted or rolled over
                        s.prev_val = 0

                    _log.debug("%s: %s=%s" % (s.device, s.metric, cur_val))

                    # Write current value into the file
                    f_out = open(f_io_name, 'w')
                    f_out.write('%d\t%d' % (s.cur_time, cur_val))
                    f_out.close()

                    yield nagiosplugin.Metric(
                        s.metric,
                        cur_val - s.prev_val,
                        context='netdev')
            else:
                line_cnt += 1

        f_data.close()


# Class which prints out the custom summary message
class NetDevInfoSummary(nagiosplugin.Summary):
    def __init__(self, storage):
        self.storage = storage

    def _print_msg(self, results):
        res = results.by_name
        key = res.keys()[0]
        val = res[key].metric.value

        return (
            '%s increased by %s in %s seconds' %
            (key, val, self.storage.cur_time - self.storage.prev_time))

    # Print custom message in the case of no problem
    def ok(self, results):
        return self._print_msg(results)

    # Print custom message in the case of problem
    def problem(self, results):
        return self._print_msg(results)


# Parse command line arguments
def parse_arguments(metrics):
    description = (
        'Nagios plugin showing network device information')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--warning', '-w',
        metavar='RANGE',
        default='@2:4',
        help='warning level (default: @2:4)')
    parser.add_argument(
        '--critical', '-c',
        metavar='RANGE',
        default='@5:',
        help='critical level (default: @5:)')
    parser.add_argument(
        '--device', '-d',
        metavar='STR',
        default='eth0',
        help='network device (default: eth0)')
    parser.add_argument(
        '--metric', '-m',
        choices=metrics,
        default='rx_errs',
        help='metric (default: rx_errs)')
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=0,
        help='verbose mode (v = warn; vv = info; vvv = debug)')
    parser.add_argument(
        '--fake', '-f',
        metavar='INT',
        type=int,
        help='fake value (for testing purpose only)')
    parser.add_argument(
        '--tmp', '-t',
        metavar='DIR',
        default='/tmp',
        help='path to the temp direcotry (defaut: /tmp)')

    return (parser.parse_args(), parser)


def main():
    # List of metrics supported by this plugin
    metrics = (
        'rx_bytes', 'rx_packets', 'rx_errs', 'rx_drop', 'rx_fifo',
        'rx_frame', 'rx_compressed', 'rx_multicast',
        'tx_bytes', 'tx_packets', 'tx_errs', 'tx_drop', 'tx_fifo',
        'tx_colls', 'tx_carrier', 'tx_compressed')

    # Parse command line arguments
    (args, parser) = parse_arguments(metrics)

    # Instance of the sharing storage
    storage = Storage(metrics, args.device, args.metric, int(time()), args.tmp)

    # Instantiate the check
    check = nagiosplugin.Check(
        NetDevInfo(storage, args.fake),
        nagiosplugin.ScalarContext('netdev', args.warning, args.critical),
        NetDevInfoSummary(storage))

    # Call the check with requested verbosity
    check.main(args.verbose)


if __name__ == '__main__':
    main()
