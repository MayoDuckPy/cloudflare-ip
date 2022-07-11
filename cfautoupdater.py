#!/usr/bin/python3
from datetime import datetime
from configparser import ConfigParser

import logging
import json
import requests
import sys


def main():
    # Setup the logger
    logging.basicConfig(
            format='[%(levelname)s] %(asctime)s ~ %(message)s',
            datefmt='%Y-%m-%d %H:%M',
            level=logging.INFO,
            stream=sys.stdout
    )

    config = ConfigParser()
    config.read('config.ini')

    config_auth_section = 'AUTH'
    zone_id   = config.get(config_auth_section, 'zone_id')
    api_token = config.get(config_auth_section, 'api_token')
    record_id = config.get(config_auth_section, 'record_id')

    config_conf_section = 'CONFIG'
    ip_request_url = config.get(config_conf_section, 'ip_request_url')

    cloudflare_api = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    a_record = requests.get(cloudflare_api, headers=headers)
    if (a_record.status_code != 200):
        return logging.error('Failed to fetch the A record data.')

    current_ip = requests.get(ip_request_url)
    if (current_ip.status_code != 200):
        return logging.error('Failed to fetch the current IP (API may be down).')

    a_record_ip = a_record.json()['result']['content']
    current_ip = current_ip.json()['ip']
    if (a_record_ip == current_ip):
        return logging.info('Record IP did not need updating.')

    # Send a PATCH request so that only the payload-specified content is
    # replaced and the entire A record is not overwritten.
    #
    # https://developers.cloudflare.com/dns/manage-dns-records/how-to/create-dns-records#edit-dns-records
    payload = {'content': current_ip}
    requests.patch(cloudflare_api, headers=headers, data=json.dumps(payload))
    logging.info(f'A record IP updated: {a_record_ip} -> {current_ip}.')

if __name__ == '__main__':
    main()
