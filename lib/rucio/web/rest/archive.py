#!/usr/bin/env python
# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Vincent Garonne, <vincent.garonne@cern.ch>, 2017

from json import dumps
from logging import getLogger, StreamHandler, DEBUG
from traceback import format_exc
from web import application, loadhook, header, InternalError

from rucio.api.did import list_archive_content
from rucio.web.rest.common import rucio_loadhook, RucioController

logger, sh = getLogger("rucio.meta"), StreamHandler()
sh.setLevel(DEBUG)
logger.addHandler(sh)

URLS = ('/(.*)/(.*)/files', 'Archive')


class Archive(RucioController):
    """ REST APIs for archive. """

    def GET(self, scope, name):
        """
        List archive content keys.

        HTTP Success:
            200 Success
        """
        header('Content-Type', 'application/x-json-stream')
        try:
            for file in list_archive_content(scope=scope, name=name):
                yield dumps(file) + '\n'
        except Exception, e:
            print format_exc()
            raise InternalError(e)


"""----------------------
   Web service startup
----------------------"""

APP = application(URLS, globals())
APP.add_processor(loadhook(rucio_loadhook))
application = APP.wsgifunc()
