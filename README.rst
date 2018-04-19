IPython Slackcast
=================

Mirrors your IPython session to Slack.

Installation
------------

Add this package to wherever IPython is loading from:

::

    pip install git+https://github.com/rbdixon/slackcaster.git

Setup
-----

Get a Slack bot token.

::

    export SLACK_BOT_TOKEN=<token>

Usage
-----

In an IPython session:

::

    %slackcast @user
    %slackcast #channel
    %slackcast off
