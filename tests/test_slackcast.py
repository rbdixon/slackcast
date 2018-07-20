#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `slackcast` package."""

import pytest

from slackcast.parser import command_parser


@pytest.mark.parametrize(
    'cmd,expected',
    [
        ['@whomever', ['@whomever']],
        ['@whomever.last', ['@whomever.last']],
        ['#whatever', ['#whatever']],
        ['off', ['off']],
        ['#whatever 1', ['#whatever', 1]],
        ['@whomever 1', ['@whomever', 1]],
        ['@whomever.last 1', ['@whomever.last', 1]],
        ['#whatever 1-2', ['#whatever', 1, 2]],
        ['@whomever 1-2', ['@whomever', 1, 2]],
        ['@whomever.last 1-2', ['@whomever.last', 1, 2]],
    ],
)
def test_parse_command(cmd, expected):
    res = command_parser.parseString(cmd)

    assert list(res) == expected
