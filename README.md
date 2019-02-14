IPython Slackcast
=================

Mirrors your IPython session to Slack.

Installation
------------

Add this package to wherever IPython is loading from:

    pip install slackcast

If you would like it to be loaded automatically whenever IPython starts add this to your default profile (`~/.ipython/profile_default/ipython_config.py`):

```{.python}
try:
    import_module('slackcast.ext')
except NameError:
    # Workaround
    c.InteractiveShellApp.extensions = ['slackcast.ext']
except ModuleNotFoundError:
    print('-= slackcast is not installed =-')
```

Usage
-----

In an IPython session:

    %load_ext slackcast.ext
    %slackcast @user
    %slackcast #channel
    %slackcast off
    %slackcast #channel 1
    %slackcast #channel 1-2


Logger
------

```.python
import logging

root_logger = logging.getLogger()
root_logger.addHandler(SlackLogger(channel='#whatever', level=logging.INFO))
```
