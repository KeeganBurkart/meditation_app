from pydantic import BaseModel

class CommentInput(BaseModel):
    feed_item_id: int
    text: str

class EncouragementInput(BaseModel):
    feed_item_id: int
    text: str

class FeedInteractionResponse(BaseModel):
    interaction_id: int
    message: str
