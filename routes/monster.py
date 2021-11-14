from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from .monsters.input_models import InputMonsterInfo as InputMonsterInfo
from .monsters.output_models import *

from pydantic import parse_file_as


router = APIRouter(prefix="/monster")


class MonsterDB:
    _monsters: dict[str, OutputMonsterInfo]

    def __init__(self):
        self._monsters = {}

    @classmethod
    def from_file(cls, path: str):
        new = cls()
        monsters = parse_file_as(list[InputMonsterInfo], path)

        for m in monsters:
            new.add(m)

        return new

    def _hash(self, monster: OutputMonsterInfo) -> str:
        key = self._normalize_key(monster.name)
        if key not in self._monsters:
            return key

        num = 1
        revd_key = key + f'-{num}'
        while revd_key in self._monsters:
            num += 1
            revd_key = key + f'-{num}'

        return revd_key

    @staticmethod
    def _normalize_key(key: str) -> str:
        return key.lower().replace(" ", "-")

    @staticmethod
    def _convert_monster(base: InputMonsterInfo) -> OutputMonsterInfo:
        output = OutputMonsterInfo(
            name=base.name,
            size=base.type.size,
            type=base.type.type,
            alignment=base.type.alignment,
            hit_points=base.health.avg,
            hit_dice=HitDice(
                count=base.health.num_dice,
                size=base.health.die_size,
                mod=base.health.mod,
            ),
            armor=Armor(
                armor_class=base.armor.armor_class,
                type=base.armor.type,
            ),
            speed=[Speed(
                amount=s.amount,
                unit=s.unit) for s in base.speeds],
            level=Level(
                challenge_rating=base.cr.cr,
                xp=int(base.cr.xp.replace(",", "")),
            ),
        )
        return output

    def add(self, monster: InputMonsterInfo):
        monster: OutputMonsterInfo = self._convert_monster(monster)
        key = self._hash(monster)
        self._monsters[key] = monster

    def get(self, key: str) -> Optional[OutputMonsterInfo]:
        key = self._normalize_key(key)
        return self._monsters.get(key)

    def list(self) -> list[str]:
        return list(self._monsters.keys())


monster_db = MonsterDB.from_file('./data/monsters.json')


@router.get("/", response_model=list[str])
def list_monsters() -> list[str]:
    return monster_db.list()


@router.get("/{monster}", response_model=OutputMonsterInfo)
def get_monster(monster: str) -> OutputMonsterInfo:
    if info := monster_db.get(monster):
        return info
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You failed your perception check. Monster '{monster}' not found")
