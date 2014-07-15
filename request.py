# Sherman Pay Jing Hao
# Saturday, 12. July 2014
# Make GET and POST request to URL

import sys

import urllib.request as url_request
import urllib.error as url_error

def get_request_url(root_url, port=80, service_url='/'):
    """
    request_url(root_url[, port=80, service_url='/']) -> string
    """

    request_str_format = "{root_url}:{port}{service_url}"
    request_str = request_str_format.format(root_url=root_url,
                                            port=port, 
                                            service_url=service_url)
    return request_str

def make_request(url='', request_type='GET', param_keys=(), param_vals=()):
    """
    make_request(url=''[, request_type='GET', params=list()]) -> Request object
    Make a HTTP request to url and returns a Request object.
    Request object is defined in python urllib.
    To obtain the response from the Request object, use urllib.urlopen(Request).
    To read the data from the response, use response.read()
    """
    if request_type == 'GET':
        url += "?"
        for idx, param_key in enumerate(param_keys):
            url += "{}={}&".format(param_key, param_vals[idx])

    return url_request.Request(url)
    
def make_mult_requests(default_url='', request_type='GET', params_table=()):
    param_keys = params_table.pop(0)
    requests = []
    for param_vals in params_table:
        requests.append(make_request(default_url, request_type, param_keys, param_vals))
    return requests

def get_response(request):
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
        
def get_mult_response(request_list):
    response_list = []
    for request in request_list:
        response_list.append(request_data(request))
    return response_list

def read_config(file_path):
    with open(file_path) as config_file:
        config_dict = eval(config_file.read())
        return config_dict

def get_requesters(config):
    return config.keys()

def request_config(config, requester):
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
