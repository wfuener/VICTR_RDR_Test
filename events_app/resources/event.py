import falcon
from falcon import HTTPUnprocessableEntity, HTTPInternalServerError, Request, Response
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from common.utils import validator
from common.utils import logger


async def event_validation(req: Request, resp: Response, self, kwargs):
    """Using the jsonschema library define what an incoming event should be like.
    If validation HTTP_422 is retured via falcon's HTTPUnprocessableEntity execution.
    If successful, the on_post code is continued.
    """
    try:
        req_data = await req.get_media()
        validate(req_data, {
            "type": "object",
            "properties": {
                    "user_id": {"format": "uuid"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
            }, "required": ["user_id", "title", "description"]
        }, validator)

    except ValidationError as err:
        raise HTTPUnprocessableEntity("Failed Validation Check", repr(err))
    except Exception as exc:
        logger.error(exc)
        raise HTTPInternalServerError("An exception occurred while parsing json")


class EventResource(object):

    async def on_get(self, req: Request, resp: Response):
        """Get event(s) by user or by the event_id"""
        user_id = req.get_param("user_id")
        event_id = req.get_param("event_id")

        if user_id:
            sql = """select * from events_tracking.event where user_id = $1"""
            results = await req.context.pg.query(sql, [user_id])

        elif event_id:
            sql = """select * from events_tracking.event where event_id = $1"""
            results = await req.context.pg.query(sql, [event_id])
            results[0] if results else {}   # return empty dict if no results
        else:
            raise falcon.HTTPBadRequest(description="You must provide either a user_id or event_id")

        resp.media = results


    @falcon.before(event_validation)
    async def on_post(self, req: Request, resp: Response):
        """Create a new event"""
        json = await req.get_media()    # get the request json

        sql = """insert into events_tracking.event (user_id, title,  description) VALUES ($1, $2, $3) RETURNING event_id"""
        result = await req.context.pg.query(sql, [str(json['user_id']), json['title'], json['description']])

        if result:
            resp.status = falcon.HTTP_201
            resp.media = result[0]  # returns {event_id: ___}
        else:
            raise falcon.HTTPInternalServerError(description="Something went wrong. Event was not created")


    async def on_delete(self, req: Request, resp: Response):
        """Delete an event"""
        event_id = req.get_param("event_id", required=True)
        sql = """delete from events_tracking.event where event_id = $1"""
        await req.context.pg.query(sql, [event_id])

        resp.media = {"message": "deleted"}


class TestResource(object):
    """This Resource only exists for the demo reasons"""

    async def on_get(self, req, resp):
        """get all users and event info. This is a convenience endpoint for dev so yyou don't have to
        connect to the database during development testing"""
        results = await req.context.pg.query("""
            select * from events_tracking."user" u inner join events_tracking.event e on u.user_id = e.user_id
        """)
        resp.media = results

