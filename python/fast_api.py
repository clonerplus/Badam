from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from typing import List
from MessageResponse import MessageResponse
from MessageQuery import sqlalchemy_init

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@postgres:5432/postgres"

engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)

SessionLocal, MessageSQL = sqlalchemy_init(engine)


@app.get("/message/{group_id}", response_model=List[MessageResponse])
async def read_message(group_id: int):
    db = SessionLocal()
    messages = (db.query(MessageSQL)
                .filter(MessageSQL.group_id == group_id)
                .order_by(MessageSQL.send_time.desc())
                .limit(10)
                .all())

    db.close()

    if not messages:
        raise HTTPException(status_code=404, detail="No messages with this group id found!")

    return [MessageResponse(
        id=message.id,
        group_id=message.group_id,
        order_num=message.order_num,
        sender_id=message.sender_id,
        body=message.body,
        send_time=str(message.send_time)
    )
        for message in messages[::-1]]
