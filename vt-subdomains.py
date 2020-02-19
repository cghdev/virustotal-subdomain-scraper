#!/usr/bin/env python3
import requests
from os import environ
import os
import sys
import json

def main(domain, apikey):
    url = 'https://www.virustotal.com/vtapi/v2/domain/report'
    params = {'apikey':apikey,'domain':domain}
    try:
        response = requests.get(url, params=params)
        jdata = response.json()
        domains = sorted(jdata['subdomains'])
    except(KeyError):
        print("No domains found for %s" % domain)
        exit(0)
    except(requests.ConnectionError):
        print("Could not connect to www.virtustotal.com", file=sys.stderr)
        exit(1)

    for domain in domains:
        print(domain)

if __name__ == '__main__':
    if len(sys.argv) != 2:
    	print("Usage: {} <domain>".format(os.path.basename(__file__), file=sys.stderr))
    	sys.exit(1)
    domain = sys.argv[1]
    apikeyfile = os.path.expanduser('~/.vtapikey')
    if environ.get('VTAPIKEY'):
        apikey = os.environ['VTAPIKEY']
    else:
        if os.path.isfile(apikeyfile):
            with open(apikeyfile, 'r') as fd:
                apikey = fd.read().strip()
        else:
            print("VTAPIKEY environment variable not set and ~/.vtapikey not found. Quitting.", file=sys.stderr)
            sys.exit(1)
    main(domain, apikey)
