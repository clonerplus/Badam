from pydantic import BaseModel


class MessageResponse(BaseModel):
    id: int
    group_id: int
    order_num: int
    sender_id: int
    body: str
    send_time: str
