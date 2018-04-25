# -*- coding: utf-8 -*-

"""Main module."""

import os
import keyring
import re
import sys

from IPython.core.magic import register_line_magic
from IPython.core.events import EventManager
from prompt_toolkit import prompt

from .caster import SlackCaster, SlackcastException

__all__ = [
    'load_ipython_extension',
]

SLACKCAST_INSTALL_URL = os.environ.get('SLACKCAST_INSTALL_URL', 'https://slackcast.devtestit.com/install')
KEY = ('slackcast', 'token')
CASTER = None

def load_ipython_extension(ip):
    global CASTER

    if CASTER is None:
        token = get_token()

        if token is not None:
            CASTER = SlackCaster(shell=ip, token=token)
            ip.events.register('pre_run_cell', CASTER.pre_run_cell)
            ip.events.register('post_run_cell', CASTER.post_run_cell)
        else:
            print('Could not find or obtain a Slack token.')

def get_token():
    # For testing
    token = os.environ.get('SLACKCAST_TOKEN', None)

    if token is None:
        token = keyring.get_password(*KEY)

    if token is None:
        raw_token = prompt(f'Visit {SLACKCAST_INSTALL_URL}, approve, and enter token: ')

        if raw_token.startswith('xoxp-'):
            token = raw_token
            keyring.set_password(*KEY, token)

    return token

@register_line_magic
def slackcast(line):
    global CASTER

    channel = line

    # TODO: Add immediate mode
    # - `%slackcast @brad test`: Send "test" to @brad
    # - `%slackcast @brad _`: Send last cell and output to @brad

    if channel == 'off':
        CASTER.set_channel(None)
        sys.stderr.write('Slackcast deactivated.\n')
    else:
        try:
            CASTER.set_channel(channel)
            sys.stderr.write(f'Slackcast transmitting on {channel}\n')
        except SlackcastException:
            sys.stderr.write(f'Could not find {channel}.\n')
