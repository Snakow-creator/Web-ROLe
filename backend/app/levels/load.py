from models.models import Level
from levels.data import levels_data

async def load_levels():
    for level in levels_data:
        if await Level.find_one(Level.level == level["level"]):
            continue
        await Level.insert_one(level)
