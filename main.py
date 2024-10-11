import json
import random

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from christmas_gift_exchange_assignment import (Member, circular_permutations,
                                                create_pairs,
                                                is_valid_all_pairs)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


@app.get("/api/members/random")
def api_members_random() -> list[str]:
    with open('./members.json') as file:
        members_raw: list[Member] = json.load(file)
        members: list[Member] = random.sample(members_raw, len(members_raw))

        for pattern in circular_permutations(members):
            pairs: list[tuple[Member, Member]] = create_pairs(pattern)
            if is_valid_all_pairs(list(pairs)):
                return list(map(lambda pair: pair[0]['name'], pairs))

        raise Exception('すべてのパターンを検証しましたが、ペアを生成できません。')
