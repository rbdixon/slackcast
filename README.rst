IPython Slackcast
=================

Mirrors your IPython session to Slack.

Installation
------------

Add this package to wherever IPython is loading from:

::

    pip install git+https://github.com/rbdixon/slackcast.git

Usage
-----

In an IPython session:

::

    %load_ext slackcast
    %slackcast @user
    %slackcast #channel
    %slackcast off
