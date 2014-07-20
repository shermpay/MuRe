import argparse
import sys
import pprint
import json
from datetime import datetime

import request
import config

VERSION = "0.8-beta"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    parser.add_argument("-o", "--output", default=sys.stdout,
                        help="output contents to OUTPUT",)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="More verbose output. Default: Off.")
    parser.add_argument("-p", "--pretty", default=0, type=int,
                         help="Pretty printing")
    parser.add_argument("-q", "--quiet", action="store_true",
                         help="Quiet mode. Minimal output.")
    args = parser.parse_args()
    if not args.quiet:
        intro()
    execute(args.config_file, args.output, args.pretty)
    
def intro():
    print("MuRe: Multiple Requesting tool {}".format(VERSION))
    # Non-zero padded dates, with 24-hour clock
    print("Datetime: {}.\n".format(datetime.now().strftime("%y-%m-%d %H:%M:%S")))

def execute(config_file, stream, pretty):
    print("* Reading config:", config_file)
    print()
    conf = config.Config(config_file)
    requesters = conf.requesters()
    for requester in requesters:
        request_conf = conf.get_requester(requester)
        service_root = request_conf['service_root']
        for service in request_conf['services'].items():
            request_url = request.get_request_url(request_conf['url'],
                                                  port=request_conf['port'], 
                                                  service_url="{}{}".format(service_root, service[0]))
            
            requests = request.make_mult_requests(default_url=request_url, 
                                                  method=service[1]['method'],
                                                  params_table=service[1]['params'])
            if (stream is sys.stdout):
                print_requests_data(requests, pretty=pretty)
            else:
                print_requests_data(requests, stream=open(stream, 'a'), pretty=pretty)

def print_requests_data(requests, stream=sys.stdout, pretty=0, verbose=False):
    if pretty:
        pp = pprint.PrettyPrinter(indent=pretty, stream=stream)
    for req in requests:
        print("[{}] {}".format(req.get_method(),req.get_full_url()), file=stream)
        # Might log HTTP error
        response = request.get_response(req)
        if req.data is not None:
            print(req.data, file=stream)
        
        if verbose:
            print('URI Scheme:', req.type)
            print('Host:', req.host)
            if req.has_header():
                print('Header:', req.get_header())

        if response is not None:
            data = json.loads(response.decode(encoding='UTF-8'))
            if pretty:
                pp.pprint(data)
            else:
                print(data, file=stream)
        else:
            print("Request failed...", file=stream)

        print(file=stream)
    
    if stream is not sys.stdout:
        stream.close()
        
if __name__ == '__main__':
    main()
