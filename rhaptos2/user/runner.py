#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###
# Copyright (c) Rice University 2012-13
# This software is subject to
# the provisions of the GNU Affero General
# Public License version 3 (AGPLv3).
# See LICENCE.txt for details.
###


"""Contains common applicatin runtime logic including commandline tools.

Author: Michael Mulich
Copyright (c) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""
import os
import sys
import argparse

from rhaptos2.user.configuration import (
    find_configuration_file,
    Configuration,
    )


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--host', default='localhost',
                    help="hostname to listen on")
parser.add_argument('--port', type=int, default=8000,
                    help="port to listen on")
parser.add_argument('--debug', action="store_true",
                    help="enable debug mode")
parser.add_argument('--config', '-c',
                    help="explicitly supply a configuration file")

def runner(app_factory, args=None):
    """Run the web application"""
    # Find the configuration file.
    config_file = args.config and args.config or find_configuration_file()
    if config_file is None:
        raise Exception("The application configuration file "
                        "could not be found")

    config = Configuration.from_file(config_file)
    app = app_factory(config)

    # This is very Flask specific, but this is the best place to run
    #   the application.
    app.run(host=args.host,
            port=args.port,
            debug=args.debug,
            use_reloader=False,
            )

def main(app_factory=None):
    """Handles the usage of `runner` from the commandline interface."""
    parser.add_argument('--application', nargs=1,
                        help="the application name for commandline discovery")

    args = parser.parse_args()
    app_name = args.application
    if app_name is not None:
        app_factory = pkg_resources.load_entry_point(app_name,
                                                     'rhaptos2', 'app_factory')
    runner(app_factory, args)

if __name__ == '__main__':
    main()

