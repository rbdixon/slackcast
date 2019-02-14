import attr
import logging

from .token import get_token
from .caster import SlackCaster

__all__ = ['SlackLogger']

log = logging.getLogger(__name__)


@attr.s
class SlackLogger(logging.Handler):

    channel = attr.ib(converter=str)
    token = attr.ib(default=None, converter=str)
    level = attr.ib(default=logging.INFO, converter=int)

    def __attrs_post_init__(self):
        super().__init__(level=self.level)
        token = get_token()

        assert token is not None, 'Could not load token for Slackcast'
        self.sc = SlackCaster(token)
        self.sc.set_channel(self.channel)

    def emit(self, record):
        self.sc.say(self.format(record))
