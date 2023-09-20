from flask import Flask, jsonify
import json
from sqlalchemy import create_engine

from dto.MessageQuery import sqlalchemy_init

app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)

Session, Message = sqlalchemy_init(engine)


@app.route("/message/<int:msg_id>", methods=['GET'])
def read_message(msg_id):
    session = Session()

    message = session.query(Message).filter(Message.msg_id == msg_id).first()
    session.close()

    if message is None:
        return jsonify({"error": "Message not found"}), 404

    message_response = {column.name: getattr(message, column.name) for column in Message.__table__.columns}

    return json.dumps(message_response), 200, {'Content-Type': 'application/json'}


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

