#!/usr/bin/python3

import json
import falcon
from datetime import datetime

from lib.const import Version, Message
from lib.utility import SystemUtility, DocumentUtility, CustomJSONEncoder
from lib.resource import BaseJsonApiResource
from lib.database import Session, News


class KikuNewsApiResource(BaseJsonApiResource):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        body = SystemUtility.get_response_base_with_body(Version.VERSION_1)

        session = Session()
        try:
            news = session.query(News).order_by(News.id.desc()).limit(3)
            news_messages = []
            for e in news:
                news_messages.append({
                    'title': e.news_title,
                    'message' : e.news_message
                })
            body['data']['data'] = news_messages
            self.logger.debug(str(news_messages))
        except Exception as e:
            self.logger.error(e)
            session.rollback()
            resp.status = falcon.HTTP_500
            SystemUtility.set_response_metadata(
                Version.VERSION_1, body, Message.RESPONSE_NG, Message.RESPONSE_DATABASE_CONNECTION_ERROR)
        finally:
            session.close()

        resp.body = json.dumps(body, cls=CustomJSONEncoder)
