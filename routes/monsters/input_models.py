from pydantic import BaseModel
from typing import Optional


class TypeInfo(BaseModel):
    size: str
    type: str
    alignment: str


class HealthInfo(BaseModel):
    avg: int
    num_dice: int
    die_size: int
    mod: int


class ArmorInfo(BaseModel):
    armor_class: int
    type: Optional[str]


class SpeedInfo(BaseModel):
    amount: int
    unit: str
    type: Optional[str]


class LevelInfo(BaseModel):
    cr: str
    xp: str


class InputMonsterInfo(BaseModel):
    name: str
    type: TypeInfo
    health: HealthInfo
    armor: ArmorInfo
    speeds: list[SpeedInfo]
    cr: LevelInfo
