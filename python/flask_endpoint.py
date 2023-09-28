from flask import Flask, jsonify
import json
from sqlalchemy import create_engine

from MessageQuery import sqlalchemy_init

app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:1234@postgres:5432/postgres"
engine = create_engine(DATABASE_URL)

Session, Message = sqlalchemy_init(engine)


@app.route("/message/<int:group_id>", methods=['GET'])
def read_message(group_id):
    with Session() as session:
        messages = (
            session.query(Message)
            .filter(Message.group_id == group_id)
            .order_by(Message.send_time.desc())
            .limit(10)
            .all()
        )

        if not messages:
            return jsonify({"error": "No messages with this group id found!"}), 404

        message_response = [
            {column.name: getattr(message, column.name) for column in Message.__table__.columns}
            for message in messages[::-1]
        ]

        return jsonify(message_response), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
