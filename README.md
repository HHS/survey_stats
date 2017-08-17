[![Build Status](https://travis-ci.org/semanticbits/survey_stats.svg?branch=develop)](https://travis-ci.org/semanticbits/survey_stats)
[![Coverage Status](https://coveralls.io/repos/github/semanticbits/survey_stats/badge.svg?branch=develop)](https://coveralls.io/github/semanticbits/survey_stats?branch=develop) 
[![Requirements Status](https://requires.io/github/semanticbits/survey_stats/requirements.svg?branch=develop)](https://requires.io/github/semanticbits/survey_stats/requirements/?branch=develop)

Overview
========

Library and webservice for replicating survey statistics for various 
CDC Survey datasets using R and the *survey* package.

Installation
------------

pip install survey-stats

Documentation
-------------

Endpoints:

GET: returns the questions in the dataset.

Response Content Type: application/json

Parameters:

Parameter: d Values: yrbss, prams, brfss Description: Specifies dataset Data Type: String

Example request: <http://localhost:7777/questions?d=prams>

GET: returns the available data that can be narrowed down using the parameters.

Response Content Type: application/json

Parameters:

Parameter: d Values: yrbss, prams, brfss Description: Specifies dataset Data Type: String

Parameter: q Values: Question ID (Example: qn32) Description: Narrow data set by question by specifying this parameter Data Type: String

Parameter: v Values: Description: Data Type: List of Strings

Parameter: f Values: Field name followed by values you are filtering for (Example: year:2001,2002) Description: Fields t
