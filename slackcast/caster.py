import attr
import sys
import html
import re

from io import StringIO
from IPython.utils.capture import capture_output
from IPython.utils.io import Tee
from slackclient import SlackClient
from functools import partialmethod
from concurrent.futures import ThreadPoolExecutor

__all__ = ['SlackCaster']

ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')


class SlackAPIException(Exception):
    pass


class SlackcastException(Exception):
    pass


@attr.s
class SlackCaster:

    token = attr.ib(repr=False)
    as_user = attr.ib(default=True)

    def __attrs_post_init__(self):
        self.orig_stdout = None
        self.sc = SlackClient(self.token)
        self.channel = None
        self.cell_input = None
        self.tp = ThreadPoolExecutor(1)
        self.history = {}

    def _capture_on(self):
        self.orig_stdout = sys.stdout
        self.buffer = StringIO()
        self.tee = Tee(self.buffer, 'stdout')
        sys.stdout = self.buffer

    def _capture_off(self):
        res = None

        if self.orig_stdout is not None:

            try:
                self.tee.flush()
                sys.stdout = self.orig_stdout
                self.orig_stdout = None

                res = self.buffer.getvalue()
            finally:
                self.tee.close()
                self.tee = None

        return res

    def _call_and_get(self, cmd, seqname, filter_key, result_key, kwargs, value):
        results = self.sc.api_call(cmd, **kwargs)

        if results['ok']:
            for item in results[seqname]:
                if item[filter_key] == value:
                    return item[result_key]

    _get_channel_id = partialmethod(
        _call_and_get,
        cmd='channels.list',
        seqname='channels',
        filter_key='name',
        result_key='id',
        kwargs={'exclude_archived': 1},
    )

    _get_im_id = partialmethod(
        _call_and_get,
        cmd='im.list',
        seqname='ims',
        filter_key='name',
        result_key='id',
        kwargs={},
    )

    _get_user_id = partialmethod(
        _call_and_get,
        cmd='users.list',
        seqname='members',
        filter_key='name',
        result_key='id',
        kwargs={},
    )

    def _format_cell(self, cell):
        cell = ansi_escape.sub('', cell)
        return html.escape(f"```{cell}```", quote=False)

    def _send(self, channel, contents):
        res = self.sc.api_call(
            'chat.postMessage',
            channel=channel,
            text=self._format_cell(contents),
            as_user=self.as_user,
        )

        if not res['ok']:
            raise SlackAPIException(res['error'])

    def _send_cell(self, cell_input=None, cell_output=None):
        if self.channel is None:
            return

        if cell_input is not None:
            self.tp.submit(self._send, self.channel, cell_input)

        if cell_output is not None:
            if len(cell_output) > 0:
                self.tp.submit(self._send, self.channel, cell_output)

    def pre_run_cell(self, info):
        if not info.raw_cell.startswith('%slackcast'):
            self.cell_input = info.raw_cell
            self._capture_on()
        else:
            self.cell_input = None

    def _store_history(self, number, cell_input=None, cell_output=None):
        self.history[number] = (cell_input, cell_output)

    def post_run_cell(self, result):
        cell_output = self._capture_off()

        # Print output to console
        if type(cell_output) == str:
            sys.stdout.write(cell_output)

        # Send input and output cells to slack
        self._store_history(result.execution_count, self.cell_input, cell_output)
        self._send_cell(self.cell_input, cell_output)

    def replay(self, channel, items):
        orig_channel = self.channel
        self.set_channel(channel)

        for idx in items:
            cell_input, cell_output = self.history[idx]
            self._send_cell(cell_input, cell_output)

        self.channel = orig_channel

    def set_channel(self, channel=None):
        # Go silent
        if channel is None:
            self.channel = None
            return

        chan_type = channel[0]
        name = channel[1:]
        channel_id = None

        if chan_type == '#':
            channel_id = self._get_channel_id(value=name)
        if chan_type == '@':
            channel_id = self._get_user_id(value=name)

        if channel_id is None:
            raise SlackcastException('Could not set channel to {channel}.')
        else:
            self.channel = channel_id

    def say(self, line):
        self._send_cell(line)
