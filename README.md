# MuRe (Multiple Requests) #
Simple tool to allow multiple quick Web Requests given an config file that specifies the request.

## Overview ##
*mure.py* is mainly developed as a testing tool for your REST services.  

With *mure.py* you can make multiple web requests to a variety of web services simply.
All you have to do is edit a config file and *mure.py* will read that config file and execute all those
requests in random order.  

**Note: Request order is random for now**

## Requirements ##
* python 3

## Installation ##
`git pull https://github.com/shermpay/MuRe.git`

## Usage ##
Using it is as simple as
```bash
$ python3 mure.py CONFIG_FILE
```
```bash
$ python3 mure.py -h
usage: mure.py [-h] [-o OUTPUT] [-v] [-p [PRETTY]] [-q] config_file

positional arguments:
  config_file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output contents to OUTPUT
  -v, --verbose         More verbose output. Default: Off.
  -p [PRETTY], --pretty [PRETTY]
                        Pretty printing
  -q, --quiet           Quiet mode. Minimal output.
```

Try it out on **examples/example.py**!

## Sample Output ##
```bash
$ python3 mure.py examples/example.py 
MuRe: Multiple Requesting tool 0.8-beta
Datetime: 14-07-20 15:28:31.

* Reading config: examples/example.py

[GET]   http://shermanpay.com:8080/uw_schedule/find_user?user_name=shermpay&

Response
========

{'student_name': 'shermpay', 'user_name': 'shermpay', 'id': 16, 'timestamp': '2014-04-03T22:38:29'}

--- End of Response ---
```

## Requests Config ##
Configuration should follow the example in **examples/example.py**

The structure of the config should be familiar to python programmers, as it is just a python dictionary.

#### Parameters ####
Parameters should be specified as the example. 
Only the `method` parameter is optional, the default value is `'GET'` if not specified.


