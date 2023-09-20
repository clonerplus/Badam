from django.http import JsonResponse, HttpResponseNotFound
from .MessageQuery import sqlalchemy_init  # Adjust the import path as needed
from sqlalchemy import create_engine
import json

DATABASE_URL = "postgresql://postgres:1234@postgres:5432/postgres"
engine = create_engine(DATABASE_URL)

Session, Message = sqlalchemy_init(engine)


def read_message(request, msg_id):
    session = Session()

    message = session.query(Message).filter(Message.msg_id == msg_id).first()
    session.close()

    if message is None:
        return HttpResponseNotFound(json.dumps({"error": "Message not found"}), content_type="application/json")

    message_response = {column.name: getattr(message, column.name) for column in Message.__table__.columns}

    return JsonResponse(message_response, json_dumps_params={'indent': 2})
