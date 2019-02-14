import pytest
import logging

from slackcast import SlackLogger


def test_as_user():
    handler = SlackLogger(channel='#whatever', level=logging.DEBUG)
    log = logging.getLogger('test')
    log.addHandler(handler)
    log.critical('Logging to Slack as user')


def test_not_as_user():
    handler = SlackLogger(channel='#whatever', level=logging.DEBUG, as_user=False)
    log = logging.getLogger('test')
    log.addHandler(handler)
    log.critical('Logging to Slack NOT as user')
