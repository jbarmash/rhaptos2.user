#!/usr/bin/env python
#! -*- coding: utf-8 -*-

###  
# Copyright (c) Rice University 2012
# This software is subject to
# the provisions of the GNU Lesser General
# Public License Version 2.1 (LGPL).
# See LICENCE.txt for details.
###


"""run.py - Launch the repo app.

Author: Paul Brian
(C) 2012 Rice University

This software is subject to the provisions of the GNU Lesser General
Public License Version 2.1 (LGPL).  See LICENSE.txt for details.
"""

import os
from optparse import OptionParser
from flask import Flask
from rhaptos2.user import APPTYPE, set_app, get_app, set_logger
from rhaptos2.common import conf



def make_app(confd):
    """Application factory function"""
    app = Flask('rhaptos2.repo')

    set_app(app)
    import rhaptos2.repo.views
    return app


def make_app(_confd):
    """Application factory function"""

    app = Flask('rhaptos2.user')
    app.config.update(_confd)
    set_app(app)  ### make available through __init__.py

    # Import the views to initialize them
    import rhaptos2.user.views
    from rhaptos2.user import backend  ## these now *should* pick up the configured app
    backend.initdb(_confd)      #set up session with engine.

    assert app == rhaptos2.user.app
    return app



def parse_args():
    parser = OptionParser()
    parser.add_option("--host", dest="host",
                      help="hostname to listen on")
    parser.add_option("--port", dest="port",
                      help="port to listen on", type="int")
    parser.add_option("--debug", dest="debug", action="store_true",
                      help="debug on.", default=False)
    parser.add_option("--conf", dest="confpath",
                      help="Path to config file.")

    (options, args) = parser.parse_args()
    return (options, args)

def main():
    """Run the application, to be used to start up one instance"""
    opts, args = parse_args()

    confd = conf.get_config(opts.confpath)
    app = make_app(confd)
    print app, "<-- Intialised app"

    # NOTE Do not use module reloading, even in debug mode, because it
    #      produces new stray processes that supervisor does not ctl.
    app.run(host=opts.host,
            port=opts.port,
            debug=opts.debug,
            use_reloader=False
            )


if __name__ == '__main__':
    main()

