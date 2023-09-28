from django.http import JsonResponse, HttpResponseNotFound
from .MessageQuery import sqlalchemy_init  # Adjust the import path as needed
from sqlalchemy import create_engine
import json

DATABASE_URL = "postgresql://postgres:1234@postgres:5432/postgres"
engine = create_engine(DATABASE_URL)

Session, Message = sqlalchemy_init(engine)


def read_message(request, group_id):
    session = Session()

    messages = (
        session.query(Message)
        .filter(Message.group_id == group_id)
        .order_by(Message.send_time.desc())
        .limit(10)
        .all()
    )
    session.close()

    if not messages:
        return HttpResponseNotFound(json.dumps({"error": "No messages with this group id found!"}),
                                    content_type="application/json")

    message_response = [
        {column.name: getattr(message, column.name) for column in Message.__table__.columns}
        for message in messages[::-1]
    ]

    return JsonResponse(message_response, safe=False, json_dumps_params={'indent': 2})
