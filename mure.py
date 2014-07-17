import sys

import request
import config

if __name__ == '__main__':
    config_file = sys.argv[1]
    print("Reading config: ", config_file)
    conf = config.read_config(config_file)
    requesters = config.requesters(conf)
    for requester in requesters:
        request_conf = config.get_requester(conf, requester)
        url = request_conf['url']
        port = request_conf['port']
        service_root = request_conf['service_root']
        for service in request_conf['services']:
            request_url = request.get_request_url(url, port=port, 
                                                  service_url="{}{}".format(service_root, service))
            
            requests = request.make_mult_requests(default_url=request_url, 
                                                  method=request_conf['services'][service]['method'],
                                                  params_table=request_conf['services'][service]['params'])
            print("Requests", requests)
            for req in requests:
                response = request.get_response(req)
                print(response)
