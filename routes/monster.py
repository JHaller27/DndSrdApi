from fastapi import APIRouter

from pydantic import BaseModel
from typing import Optional


router = APIRouter(prefix="/monster")


# region Models

class HitDice(BaseModel):
    count: int
    size: int
    mod: int


class Armor(BaseModel):
    armor_class: int
    type: str


class Speed(BaseModel):
    amount: int
    unit: str


class MonsterInfo(BaseModel):
    name: str
    size: str
    type: str
    alignment: tuple[str, str]
    hit_points: int
    hit_dice: HitDice
    armor: Armor
    speed: list[Speed]
    challenge_rating: str  # Str b/c CR could be "1/2", and don't want to deal w/ floating-point errors

# endregion


class MonsterDB:
    _monsters: dict[str, MonsterInfo]

    def __init__(self):
        self._monsters = {}

    def _hash(self, monster: MonsterInfo) -> str:
        return monster.name

    def add(self, monster: MonsterInfo):
        key = self._hash(monster)
        self._monsters[key] = monster

    def get(self, key: str) -> Optional[str]:
        return self._monsters.get(key)


@router.get("/list", response_model=list[tuple[str, MonsterInfo]])
def list_monsters() -> list[tuple[str, MonsterInfo]]:
    return []
