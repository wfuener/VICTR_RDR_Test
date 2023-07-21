import falcon.asgi
from dotenv import load_dotenv

from resources.event import EventResource, TestResource
from resources.search import SearchResource

from middleware import *

# load env variables
load_dotenv()

# create middleware objects
middleware = [RequestLoggerMiddleware(), DBMiddleware(), AuthMiddleware()]


# Initialize app and attach middleware to it
api = falcon.asgi.App(middleware=middleware)

# add extras to falcon app:  Request, Response, and error handling extras
api.req_options.media_handlers.update(extra_handlers)
api.resp_options.media_handlers.update(extra_handlers)
api.add_error_handler(Exception, handle_uncaught_exception)


class Ping:
    """Simple get resource to check if api is up and running."""

    async def on_get(self, req, resp):
        resp.media = "Ping"


# define routes
api.add_route('/', Ping())
api.add_route('/test-data', TestResource())
api.add_route('/event', EventResource())
api.add_route('/search', SearchResource())



