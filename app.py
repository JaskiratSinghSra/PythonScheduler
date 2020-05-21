"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import time
import os
import requests

from apscheduler.schedulers.background import BackgroundScheduler

health_url = "http://localhost:5000/user/health"
slack_url = "https://hooks.slack.com/services/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"

fail_response = {
    "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#8B0000",
            "text": "API not reachable",
            "fields": [
                {
                    "title": "Severity",
                    "value": "High",
                    "short": False
                }
            ],
            "footer": "Slack API",
            "ts": 123456789
        }
    ]
}
headers = {
    'Content-Type': 'application/json'
}


def health_check():
    response = requests.request("POST", slack_url, headers=headers, json=fail_response)
    print(response)


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(health_check, 'interval', seconds=5)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
