from typing import Optional, List

from pydantic import BaseModel, validator
from core.enumerations import recommendations

class Season(BaseModel):
    value: str
    label: str

    class Config:
        use_enum_values = True

# Shared properties
class TravelRecommendationBase(BaseModel):
    country: str
    season: Optional[str] = None

class TravelRecommendationCreate(TravelRecommendationBase):
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
