import falcon
from falcon import HTTPUnprocessableEntity, HTTPInternalServerError, Request, Response
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from common.utils import validator
from common.utils import logger


async def event_validation(req: Request, resp: Response, self, kwargs):
    """Using the jsonschema library define what an incoming menu should be like.
    If validation HTTP_422 is retured via falcon's HTTPUnprocessableEntity execution.
    If successful, the on_post code is continued.
    """
    try:
        req_data = await req.get_media()
        validate(req_data, {
            "type": "object",
            "properties": {
                    "user_id": {"type": "string"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
            }, "required": ["title", "description"]
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

        else:
            raise falcon.HTTPBadRequest(description="You must provide either a user_id or event_id")

        resp.media = results


    # @falcon.before(event_validation)
    async def on_post(self, req: Request, resp: Response):
        """Create a new event"""
        json = await req.get_media()    # get the request json

        sql = """insert into events_tracking.event (user_id, title,  description) VALUES ($1, $2, $3) RETURNING event_id"""
        result = await req.context.pg.query(sql, [str(json['user_id']), json['title'], json['description']])

        if result:
            resp.status = falcon.HTTP_201
            resp.media = {"event_id": result[0]}
        else:
            raise falcon.HTTPInternalServerError(description="Something went wrong. Event was not created")



    async def on_delete(self, req: Request, resp: Response):
        """Delete an event"""
        event_id = req.get_param("event_id", required=True)
        sql = """delete from events_tracking.event where event_id = $1"""
        await req.context.pg.query(sql)

        resp.media = {"message": "deleted"}
