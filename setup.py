# -*- coding: utf-8 -*-
from setuptools import setup
import sys
import unittest

import croniter
from croniter import __version__, __license__, __author__

if __name__ == '__main__':
  from croniter import croniter_test
  # run module test
  loader = unittest.TestLoader()
  result = unittest.TestResult()
  suite  = loader.loadTestsFromModule(croniter_test)
  suite.run(result)
  if not result.wasSuccessful():
    print "unit tests have failed!"
    print "aborted to make a source distribution"
    sys.exit(1)

  # build distribution package
  setup(
    packages         = ('croniter',),
    name             = 'croniter',
    version          = __version__,
    py_modules       = ['croniter', 'croniter_test'],
    description      = 'croniter provides iteration for datetime object with cron like format',
    long_description = croniter.__doc__,
    author           = __author__,
    author_email     = 'taichino@gmail.com',
    url              = 'http://github.com/taichino/croniter',
    keywords         = 'datetime, iterator, cron',
    license          = __license__,
    classifiers      = ["Development Status :: 3 - Alpha",
                        "Intended Audience :: Developers",
                        "License :: OSI Approved :: MIT License",
                        "Operating System :: POSIX",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Libraries :: Python Modules"]
    )
