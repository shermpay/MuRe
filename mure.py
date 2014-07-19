import argparse
import sys
import pprint
import json

import request
import config

def print_requests_data(requests, file=sys.stdout, verbose=False):
    pp = pprint.PrettyPrinter(indent=1, stream=file)
    for req in requests:
        response = request.get_response(req)
        pp.pprint("[{}] {}".format(req.get_method(),req.get_full_url()))
        if (req.data is not None):
            pp.pprint(req.data)

        pp.pprint(response)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    parser.add_argument("-o", "--output", help="output contents to OUTPUT")
    parser.add_argument("-v", "--verbose", action="store_true", help="More verbose output. Default: Off.")
    args = parser.parse_args()

    print("Reading config: ", args.config_file)
    conf = config.read_config(args.config_file)
    requesters = config.requesters(conf)
    for requester in requesters:
        request_conf = config.get_requester(conf, requester)
        service_root = request_conf['service_root']
        for service in request_conf['services']:
            request_url = request.get_request_url(request_conf['url'],
                                                  port=request_conf['port'], 
                                                  service_url="{}{}".format(service_root, service))
            
            requests = request.make_mult_requests(default_url=request_url, 
                                                  method=request_conf['services'][service]['method'],
                                                  params_table=request_conf['services'][service]['params'])
            print_requests_data(requests)

    
