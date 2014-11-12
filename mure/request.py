# Author: Sherman Pay Jing Hao
# Version: 0.1; Saturday, 12. July 2014

# stdlib Modules
from sys import stderr
import urllib.request as url_request
import urllib.error as url_error
import urllib.parse as url_parse

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
    query = url_parse.urlencode(params)
    if method == 'GET':
        url += "?" + query
        return url_request.Request(url, method=method)
    elif method == 'POST':
        hdrs = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                "Content-Length": len(query)}
        return url_request.Request(url, data=bytes(query, "utf-8"),
                                   headers=hdrs, method=method)
        
def make_mult_requests(default_url, method='GET', params_table=[], times=1):
    """
    make_mult_requests(default_url[, method='get', paramas_table=[]]) -> list of request object
    make a http request to url with parameters specified in params_table.
    params_table should have the param_keys as a tuple/list in the 0th index.
    and each individual row should map the values to the keys by column index.
    returns a list of request objects.
    """
    param_keys = params_table[0]
    requests = [make_request(default_url, method, dict(zip(param_keys, param_vals))) 
              for param_vals in params_table[1:(len(params_table))]]
    result = []
    for r in requests:
        for t in range(times):
            result.append(r)
    return result

def get_response(request, proxy=None):
    """
    get_response(request) -> string
    trys to obtain data from request object.
    outputs error messages to stderr if http error was encountered
    """
    if (proxy is not None):
        print('proxy: {}'.format(proxy))
        proxy_handler = url_request.ProxyHandler({'http': 'http://54.224.82.100:80'})
        url_request.install_opener(url_request.build_opener(proxy_handler))
    try:
        response = url_request.urlopen(request)
    except url_error.URLError as err:
        print("{}: {}".format(err, request.get_full_url()), file=stderr)
    else:
        return response
        
def get_mult_response(request_list):
    """
    get_mult_response(request_list) -> list of strings
    Trys to obtain responses from list of Request objects.
    Returns a list of Response objects.
    Outputs error messages to stderr if HTTP error was encountered.
    """
    response_list = []
    return [request_data(request) for request in request_list]

