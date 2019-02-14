import os
import keyring
from prompt_toolkit import prompt

KEY = ('slackcast', 'token')
SLACKCAST_INSTALL_URL = os.environ.get(
    'SLACKCAST_INSTALL_URL', 'https://slackcast.devtestit.com/install'
)


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

