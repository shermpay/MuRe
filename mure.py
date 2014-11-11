""" Main Driver for MuRe"""
import argparse
import sys
import pprint
import json
from datetime import datetime

import mure.request as request
import mure.config as config

VERSION = "0.8-beta"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file")
    parser.add_argument("-o", "--output", default=sys.stdout,
                        help="output contents to OUTPUT",)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="More verbose output. Default: Off.")
    parser.add_argument("-i", "--indent", default=0, type=int, nargs='?', const=1,
                         help="Pretty printing with INDENT")
    parser.add_argument("-q", "--quiet", action="store_true",
                         help="Quiet mode. Minimal output.")
    parser.add_argument("-p", "--proxy", help="Make requests with PROXY")
    args = parser.parse_args()
    if not args.quiet:
        intro()
    if args.proxy is not None:
        protocol, addr, port = args.proxy.split(':')
        args.proxy = {protocol: "{}:{}".format(addr, port)}
    exec_args = {'stream': args.output, 'indent': args.indent, 'verbose': args.verbose, 'proxy': args.proxy}
    execute(args.config_file, **exec_args)
    
def intro():
    print("MuRe: Multiple Requesting tool {}".format(VERSION))
    # Non-zero padded dates, with 24-hour clock
    print("Datetime: {}.\n".format(datetime.now().strftime("%y-%m-%d %H:%M:%S")))

def execute(config_file, **kwargs):
    print("* Reading config:", config_file)
    print()
    conf = config.Config(config_file)
    requesters = conf.requesters()
    key = config.Config.Key
    for requester in requesters:
        request_conf = conf.get_requester(requester)
        service_root = request_conf[key.service_root]
        for service_path, service_conf in request_conf[key.services].items():
            service_str = "{}{}".format(service_root, service_path)
            request_url = request.get_request_url(request_conf[key.url],
                                                  port=request_conf[key.port], 
                                                  service_url=service_str)
            
            request_times = request_conf[config.Config.Key.times]
            for n in range(request_times):
                requests = request.make_mult_requests(default_url=request_url, 
                                                  method=service_conf[key.method],
                                                  params_table=service_conf[key.params])
            
                if (kwargs['stream'] is not sys.stdout):
                    kwargs['stream'] = open(stream, 'a')

                print_requests_data(requests, **kwargs)


# Loops through Request data and outputs them
def print_requests_data(requests, **kwargs):
    # Kwargs for different output
    stream = kwargs['stream']
    pretty = kwargs['indent']
    verbose = kwargs['verbose']
    proxy = kwargs['proxy']

    if pretty:
        pp = pprint.PrettyPrinter(indent=pretty, stream=stream)
    for req in requests:
        print("[{}]\t{}".format(req.get_method(),req.get_full_url()), file=stream)
        if proxy is not None:
            print("Proxy: {}".format(proxy))
        # Might log HTTP error
        response = request.get_response(req, proxy)
        if verbose:
            print('\tURI Scheme:', req.type)
            print('\tHost:', req.host)
            print('\tHeaders: ', req.header_items())

        if req.data is not None:
            print(req.data, file=stream)

        if response is not None:
            data = response.read()
            info = response.info()
            
            if (info.get_content_subtype() == 'json'):
                data = json.loads(data.decode(encoding='UTF-8'))
            print('\nResponse')
            print('========\n')
            if verbose:
                print('Info:', info)
            if pretty:
                pp.pprint(data)
            else:
                print(data, file=stream)
        else:
            print("Request failed...", file=stream)

        print(file=stream)
        print('--- End of Response ---\n', file=stream)
    
    if stream is not sys.stdout:
        stream.close()
        
if __name__ == '__main__':
    main()
