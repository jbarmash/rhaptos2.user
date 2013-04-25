#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""Contains a common configuration parsing class and various utilities for
dealing with configuration.

Author: Michael Mulich
Copyright (c) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
from collections import Mapping
from ConfigParser import RawConfigParser


DEFAULT_APP_NAME = 'app'


def find_configuration_file():
    """A way to automatically discovery/find a configuration file using
    a constant set of path locations.

    """
    return None


class Configuration(Mapping):
    """A configuration settings object"""

    def __init__(self, settings={}, global_settings={}):
        self._settings = settings
        self._settings['globals'] = global_settings

    @classmethod
    def from_file(cls, file, app_name=DEFAULT_APP_NAME):
        """Initialize the class from an INI file."""
        settings = {}
        global_settings = {}
        with open(file, 'r') as f:
            config = RawConfigParser()
            config.readfp(f)
            for section in config.sections():
                if section == app_name:
                    settings.update(config.items(section))
                else:
                    global_settings[section] = dict(config.items(section))
        return cls(settings, global_settings)

    def __getitem__(self, key):
        return self._settings[key]

    def __setitem__(self, key, val):
        self._settings.__setitem__(key,val)

    def __delitem__(self, key):
        self._settings.__delitem__(key)

    def __len__(self):
        return len(self._settings)

    def __iter__(self):
        return self._settings.__iter__()

    def __repr__(self):
        return repr(self._settings)

