"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
import requests
from response import okay_response, fail_response
from apscheduler.schedulers.background import BackgroundScheduler

health_url = "http://localhost:5000/user/health"
slack_url = "https://hooks.slack.com/services/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"


headers = {
    'Content-Type': 'application/json'
}


def health_check():
    response = requests.request("GET", health_url, headers={})
    if response.status_code != 200:
        requests.request("POST", slack_url, headers=headers, json=fail_response)
    else:
        response= requests.request("POST", slack_url, headers=headers, json=okay_response)
        print(response)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(health_check, 'interval', minutes=1)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
