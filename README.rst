========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/survey_stats/badge/?style=flat
    :target: https://readthedocs.org/projects/survey_stats
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/uhjish/survey_stats.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/uhjish/survey_stats

.. |requires| image:: https://requires.io/github/uhjish/survey_stats/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/uhjish/survey_stats/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/uhjish/survey_stats/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/uhjish/survey_stats

.. |version| image:: https://img.shields.io/pypi/v/survey-stats.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/survey-stats

.. |downloads| image:: https://img.shields.io/pypi/dm/survey-stats.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/survey-stats

.. |wheel| image:: https://img.shields.io/pypi/wheel/survey-stats.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/survey-stats

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/survey-stats.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/survey-stats

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/survey-stats.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/survey-stats


.. end-badges

A package wrapping R survey package using Rpy2, with some helper methods for CDC survey data.

* Free software: BSD license

Installation
============

::

    pip install survey-stats

Documentation
=============


Endpoints:

GET '/questions'

Returns the questions in the dataset.

Response Content Type: application/json

Parameters:

Parameter: d
Values: yrbss, prams, brfss
Description: Specifies dataset
Data Type: String

Example request: http://localhost:7777/questions?d=prams

GET '/stats'

Returns the available data that can be narrowed down using the parameters.

Response Content Type: application/json

Parameters:

Parameter: d
Values: yrbss, prams, brfss
Description: Specifies dataset
Data Type: String

Parameter: q
Values: Question ID (Example: qn32)
Description: Narrow data set by question by specifying this parameter
Data Type: String

Parameter: v
Values:
Description:
Data Type: List of Strings

Parameter: f
Values: Field name followed by values you are filtering for (Example: year:2001,2002)
Description: Fields to filter the data set by
Data Type: Field name followed by a colon followed by a list of values separated by commas. Each set of field name and values separated by a pipe (Example: f=year:2001,2002|sitecode:IL)

Parameter: s
Values: 1, 2
Description: Specifies if you want to the precomputed data set (s=1) or raw data (s=2)
Data Type: Integer

Example request: http://localhost:7777/stats?d=prams&f=year:2001,2002|sitecode:IL&q=qn25&s=1&v=sitecode,year

https://survey_stats.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
