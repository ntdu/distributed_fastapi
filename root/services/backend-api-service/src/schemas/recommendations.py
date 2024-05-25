from typing import Optional, List
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel
from pydantic import BaseModel, validator, Field
from typing import List, Optional
from core.enumerations import recommendations

class Season(BaseModel):
    value: str
    label: str

    class Config:
        use_enum_values = True

# Shared properties
class ThingsHistoryBase(BaseModel):
    # _id: Optional[UUID] = None
    country: str
    season: Optional[str] = None

class ThingsHistoryCreate(ThingsHistoryBase):
    season: str

    @validator('season')
    def season_must_be_valid(cls, v):
        valid_seasons = [
            recommendations.Season.SPRING.value,
            recommendations.Season.SUMMER.value,
            recommendations.Season.FALL.value,
            recommendations.Season.WINTER.value]

        if v not in valid_seasons:
            raise ValueError(f'Season must be one of: {valid_seasons}')
        return v
