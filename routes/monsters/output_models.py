from pydantic import BaseModel
from typing import Optional


class HitDice(BaseModel):
    count: int
    size: int
    mod: int


class Armor(BaseModel):
    armor_class: int
    type: Optional[str]


class Speed(BaseModel):
    amount: int
    unit: str


class Level(BaseModel):
    challenge_rating: str  # Str b/c CR could be "1/2", and don't want to deal w/ floating-point errors
    xp: int


class OutputMonsterInfo(BaseModel):
    name: str
    size: str
    type: str
    alignment: str
    hit_points: int
    hit_dice: HitDice
    armor: Armor
    speed: list[Speed]
    level: Level
