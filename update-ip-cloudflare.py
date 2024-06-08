#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys

IP_API = 'https://api.ipify.org?format=json' # get Public IP Server
CF_API_KEY = 'Global API Key From nenu My Profile'
CF_EMAIL = 'Username of Cloudflare'
ZONE_ID = 'Zone ID of Domain name in Dashboard Cloudflare'
DOMAIN = 'Your Domain name'
RECORD_ID = 'RECORD_ID is show first time for run this script'


if not RECORD_ID:
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    print('Please copy your DNS record ID into the script')
    RECORD_ID = resp.json()['result'][0]['id']
    print(RECORD_ID)
    sys.exit(0)

resp = requests.get(IP_API)
ip = resp.json()['ip']

resp = requests.put(
    'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
        ZONE_ID, RECORD_ID),
    json={
        'type': 'A',
        'name': 'weaq.cc',
        'content': ip,
        'proxied': True #False
    },
    headers={
        'X-Auth-Key': CF_API_KEY,
        'X-Auth-Email': CF_EMAIL
    })
assert resp.status_code == 200

print('Updated dns record for {}'.format(ip))
