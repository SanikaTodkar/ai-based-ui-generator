from pydantic import BaseModel, Field
from typing import List, Dict, Any


class UINode(BaseModel):
    type: str
    props: Dict[str, Any] = Field(default_factory=dict)
    children: List["UINode"] = Field(default_factory=list)


UINode.model_rebuild()
