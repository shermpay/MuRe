# Author: Sherman Pay Jing Hao
# Version: 0.1; Saturday, 12. July 2014

# stdlib Modules
from sys import stderr
import urllib.request as url_request
import urllib.error as url_error

""" 
Make GET and POST request to various web services.
This module is very functional instead of imperative.
Use this module to obtain list of multiple Request objects,
and then execute on that list.

Future implementations would use lazy sequences/generators.
Therefore this implementation is NOT final.
"""

def get_request_url(root_url, port=80, service_url='/'):
    """
    request_url(root_url[, port=80, service_url='/']) -> string
    Transforms the url into a url that points to a request, given the parameters.
    """
    request_str_format = "{root_url}:{port}{service_url}"
    request_str = request_str_format.format(root_url=root_url,
                                            port=port, 
                                            service_url=service_url)
    return request_str

def make_request(url, method='GET', params={}):
    """
    make_request(url[, method='GET', params={}]]) -> Request object
    Make a HTTP request to url with param.keys()=params.values() as request parameters.
    Returns a Request object.
    Request object is defined in python urllib.
    To obtain the response from the Request object, use urllib.urlopen(Request).
    To read the data from the response, use response.read()
    """
    if method == 'GET':
        url += "?"
        for param_key, param_val in params.items():
            url += "{}={}&".format(param_key, param_val)
        return url_request.Request(url)
    elif method == 'POST':
        return url_request.Request(url, params)
        
def make_mult_requests(default_url, method='GET', params_table=[]):
    """
    make_mult_requests(default_url[, method='GET', paramas_table=[]]) -> list of Request object
    Make a HTTP request to url with parameters specified in params_table.
    params_table should have the param_keys as a tuple/list in the 0th index.
    And each individual row should map the values to the keys by column index.
    Returns a list of Request objects.
    """
    param_keys = params_table.pop(0)
    return [make_request(default_url, method, dict(zip(param_keys, param_vals))) 
            for param_vals in params_table]

def get_response(request):
    """
    get_response(request) -> string
    Trys to obtain data from Request object.
    Outputs error messages to stderr if HTTP error was encountered
    """
    try:
        response = url_request.urlopen(request)
    except url_error.URLError as err:
        print("{}: {}".format(err, request.get_full_url()), file=stderr)
    else:
        response_data = response.read()
        return response_data
        
def get_mult_response(request_list):
    """
    get_mult_response(request_list) -> list of strings
    Trys to obtain responses from list of Request objects.
    Returns a list of Response objects.
    Outputs error messages to stderr if HTTP error was encountered.
    """
    response_list = []
    return [request_data(request) for request in request_list]

