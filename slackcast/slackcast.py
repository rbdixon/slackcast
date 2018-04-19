# -*- coding: utf-8 -*-

"""Main module."""

import os

from IPython.core.magic import register_line_magic
from IPython.core.events import EventManager

from .caster import SlackCaster

__all__ = [
    'load_ipython_extension',
]

SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
CASTER = None

def load_ipython_extension(ip):
    global CASTER

    if CASTER is None:
        CASTER = SlackCaster(shell=ip, token=SLACK_BOT_TOKEN)
        ip.events.register('pre_run_cell', CASTER.pre_run_cell)
        ip.events.register('post_run_cell', CASTER.post_run_cell)

@register_line_magic
def slackcast(line):
    global CASTER

    channel = line

    if channel == 'off':
        res = CASTER.set_channel(None)
    else:
        res = CASTER.set_channel(channel)

    print(res)
