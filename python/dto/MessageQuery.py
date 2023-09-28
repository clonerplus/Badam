from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def sqlalchemy_init(engine):
    sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    base = declarative_base()

    class Message(base):
        __tablename__ = "chatroom"

        id = Column(Integer, primary_key=True, index=True)
        group_id = Column(Integer, index=True)
        order_num = Column(Integer)
        sender_id = Column(Integer)
        body = Column(String)
        send_time = Column(String)

    base.metadata.create_all(bind=engine)

    return sessionLocal, Message
