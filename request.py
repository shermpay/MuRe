# Sherman Pay Jing Hao
# Saturday, 12. July 2014
# Make GET and POST request to URL

import sys

import urllib.request as url_request
import urllib.error as url_error

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

def make_request(url, request_type='GET', params={}):
    """
    make_request(url[, request_type='GET', params={}]]) -> Request object
    Make a HTTP request to url with param.keys()=params.values() as request parameters.
    Returns a Request object.
    Request object is defined in python urllib.
    To obtain the response from the Request object, use urllib.urlopen(Request).
    To read the data from the response, use response.read()
    """
    if request_type == 'GET':
        url += "?"
        for param_key, param_val in params.items():
            url += "{}={}&".format(param_key, param_val)

    return url_request.Request(url)
    
def make_mult_requests(default_url, request_type='GET', params_table=[]):
    """
    make_mult_requests(default_url[, request_type='GET', paramas_table=[]]) -> list of Request object
    Make a HTTP request to url with parameters specified in params_table.
    params_table should have the param_keys as a tuple/list in the 0th index.
    And each individual row should map the values to the keys by column index.
    Returns a list of Request objects.
    """
    param_keys = params_table.pop(0)
    return [make_request(default_url, request_type, dict(zip(param_keys, param_vals))) 
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
        print("{} was caught. Reason: {}".format(err, err.reason), file=sys.stderr)
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

def read_config(file_path):
    """
    read_config(file_path) -> dict
    Reads config from file_path
    Returns a dict that holds the configuration
    """
    url='url'
    port='port'
    services='services'
    service_root='service_root'
    request_type='request_type'
    with open(file_path) as config_file:
        config_dict = eval(config_file.read())
        return config_dict

def get_requesters(config):
    """
    get_requesters(config) -> set
    Returns a set of requesters
    """
    return config.keys()

def request_config(config, requester):
    """
    request_config(config, requester) -> dict
    Returns a particular configuration for a requester given the config_dict
    """
    return config[requester]

if __name__ == '__main__':
    config_file = sys.argv[1]
    print("Reading config: ", config_file)
    config = read_config(config_file)
    requesters = get_requesters(config)
    for requester in requesters:
        request_conf = request_config(config, requester)
        url = request_conf['url']
        port = request_conf['port']
        service_root = request_conf['service_root']
        for service in request_conf['services']:
            request_url = get_request_url(url, port=port, 
                                          service_url="{}{}".format(service_root, service))
            
            requests = make_mult_requests(default_url=request_url, 
                                          request_type=request_conf['request_type'],
                                          params_table=request_conf['services'][service])
            print("Requests", requests)
            for request in requests:
                response = get_response(request)
                print(response)
