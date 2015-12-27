# -----------------------------------------------------------------------------
# Copyright (c) 2009-2016 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
import logging
log = logging.getLogger('glumpy')
log.setLevel(logging.INFO)
# log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

# create formatter
# formatter = logging.Formatter('%(levelname)s: %(message)s')
# formatter = logging.Formatter('%(message)s')
class Formatter(logging.Formatter):
    def format(self, record):
        prefix = {logging.INFO    : "[i]",
                  logging.WARNING : "[w]",
                  logging.ERROR   : "[e]",
                  logging.CRITICAL: "[x]"}
        if record.levelno in (
                logging.INFO,
                logging.WARNING,
                logging.ERROR,
                logging.CRITICAL):
            # record.msg = '[%s] %s' % (record.levelname, record.msg)
            record.msg = '%s %s' % (prefix[record.levelno], record.msg)
        return super(Formatter , self).format(record)
formatter = Formatter('%(message)s')


# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)

# log.debug('debug message')
# log.info('info message')
# log.warn('warn message')
# log.error('error message')
# log.critical('critical message')
