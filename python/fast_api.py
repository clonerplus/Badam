from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from dto.MessageResponse import MessageResponse
from dto.MessageQuery import sqlalchemy_init

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal, MessageSQL = sqlalchemy_init(engine)


@app.get("/message/{msg_id}", response_model=MessageResponse)
async def read_message(msg_id: int):
    db = SessionLocal()
    message = db.query(MessageSQL).filter(MessageSQL.msg_id == msg_id).first()
    db.close()
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return MessageResponse(msg_id=message.msg_id,
                           order_num=message.order_num,
                           sender_id=message.sender_id,
                           body=message.body,
                           send_time=str(message.send_time))


@app.get("/fastapi")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
