# Sherman Pay Jing Hao
# Saturday, 12. July 2014
# Make GET and POST request to URL

import sys

import urllib.request as url_request
import urllib.error as url_error

def request_url(root_url, port=80, service_url='/'):
    """
    request_url(root_url[, port=80, service_url='/']) -> string
    """

    request_str_format = "{root_url}:{port}{service_url}"
    request_str = request_str_format.format(root_url=root_url,
                                            port=port, 
                                            service_url=service_url)
    return request_str

def make_request(url='', request_type='GET', params=list()):
    """
    make_request(url=''[, request_type='GET', params=list()]) -> Request object
    Make a HTTP request to url and returns a Request object.
    Request object is defined in python urllib.
    To obtain the response from the Request object, use urllib.urlopen(Request).
    To read the data from the response, use response.read()
    """
    if request_type == 'GET':
        request_str += "?"
        for param_key in params.keys():
            request_str += "{}={}&".format(param_key, params[param_key])

    return url_request.Request(url)
    

def get_request_data(request):
    """
    get_request_data(request) -> string
    Trys to obtain data from request.
    Outputs error messages to stderr if HTTP error was encountered
    """
    try:
        response = url_request.urlopen(request)
    except url_error.URLError as err:
        print("{} was caught. Reason: {}".format(err, err.reason), file=sys.stderr)
    else:
        response_data = response.read()
        return response_data

def parse_config(file_path):
    with open(file_path) as config_file:
        config_dict = eval(config_file.read())
        return config_dict

if __name__ == '__main__':
    config = sys.argv[1]
    print("Parsing config: ", config)
    parse_config(config)
