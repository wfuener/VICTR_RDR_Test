import falcon.media
from common.utils import *

# search for both a title and description
TITLE_DESCRIPTION_SEARCH = """
    SELECT
        events_tracking.event.event_id,
        events_tracking.event.title,
        events_tracking.event.description,
        ts_rank,
        similarity
    FROM
        events_tracking.event,
        -- create ts vector (inverted index) of both values
        to_tsvector(events_tracking.event.title || events_tracking.event.description) document,
        to_tsquery($1) query,
        -- exact matches on query as tokenized values
        nullif(ts_rank(document, query),0) ts_rank,
        -- fuzzy matching on title and description
        SIMILARITY($1, events_tracking.event.title || events_tracking.event.description) similarity
    WHERE user_id = $2 AND (
        -- either an exact match or fuzzy matching score greater then 0
          query @@ document OR ts_rank> 0 OR similarity > 0
    )
    ORDER BY ts_rank, similarity DESC
"""

# search for a title
TITLE_SEARCH = """
    SELECT
        events_tracking.event.event_id,
        events_tracking.event.title,
        events_tracking.event.description,
        ts_rank,
        similarity
    FROM
        events_tracking.event,
        to_tsquery($1) query,

        ts_rank(ts_title, query) ts_rank,

        SIMILARITY($1, events_tracking.event.title) similarity
    WHERE user_id = $2 AND (
        -- either an exact match or fuzzy matching score greater then 0
        query @@ ts_title  OR ts_rank > 0 OR  similarity > 0
    )
    ORDER BY ts_rank, similarity DESC
"""

# search for a description
DESCRIPTION_SEARCH = """
    SELECT
        events_tracking.event.event_id,
        events_tracking.event.title,
        events_tracking.event.description,
        ts_rank,
        similarity
    FROM
        events_tracking.event,
        to_tsquery($1) query,

        ts_rank(ts_description, query) ts_rank,

        SIMILARITY($1, events_tracking.event.title) similarity
    WHERE user_id = $2 AND (
        -- either an exact match or fuzzy matching score greater then 0
        query @@ ts_description  OR ts_rank > 0 OR  similarity > 0
    )
    ORDER BY ts_rank, similarity DESC
"""


class SearchResource(object):


    async def on_get(self, req, resp):
        """Search events for either title or description """
        user_id = req.get_param("user_id", required=True)
        query = req.get_param("query", required=True)
        _type = req.get_param("type", required=True)

        if _type not in (["description", "title", "both"]):
            raise falcon.HTTPBadRequest(description="Invalid search type")

        elif _type == "both":
            results = await req.context.pg.query(TITLE_DESCRIPTION_SEARCH, [query, user_id])

        elif _type == "title":
            results = await req.context.pg.query(TITLE_SEARCH, [query, user_id])

        elif _type == "description":
            results = await req.context.pg.query(DESCRIPTION_SEARCH, [query, user_id])

        resp.media = results




