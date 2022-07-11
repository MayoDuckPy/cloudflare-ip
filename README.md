# Cloudflare DNS Auto IP Updater

A fork of [pigeonburger/cloudflare-ip](https://github.com/pigeonburger/cloudflare-ip)
modified to run only once so that it can be used with systemd or cron.
Additionally, logs are now sent to stdout and the emailer has been removed.

Be aware, **this only works if your site is on the Cloudflare CDN**.
See the requirements below:

## Requirements

- Python 3.6 or above
- Python `requests` library (if Python version <3.7)
- Cloudflare API Token
- Cloudflare Zone ID
- Cloudflare Record ID
 
## Installation

1. Clone the repository.
2. Modify `config.ini` to match your configuration.
3. Run the script with `python3 cfautoupdater.py`.
