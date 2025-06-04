from pydantic import BaseModel


class CommentInput(BaseModel):
    """Input payload for commenting on a feed item."""

    feed_item_id: int
    text: str


class EncouragementInput(BaseModel):
    """Input payload for sending encouragement related to a feed item."""

    feed_item_id: int
    text: str


class FeedInteractionResponse(BaseModel):
    """Response returned after creating a comment or encouragement."""

    interaction_id: int
    message: str
