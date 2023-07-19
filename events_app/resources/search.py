import falcon.media
from common.utils import *


class SearchResource(object):

    async def on_get(self, req, resp):
        title = req.get_param("title")
        description = req.get_param("description")

        if not title and not description:
            raise falcon.HTTPBadRequest(description="title or description must be given")


