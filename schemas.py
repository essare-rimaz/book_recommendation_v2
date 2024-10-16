from pydantic import BaseModel


class RecommendationOut(BaseModel):
    ISBN: str
    TITLE: str
    TITLE_LOWERCASE: str
    PUBLICATION_YEAR: int
    PUBLISHER: str