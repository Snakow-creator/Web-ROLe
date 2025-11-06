from models.models import User

from datetime import datetime

async def str_to_datetime():
    for user in await User.find().to_list():
      user.last_streak = datetime.strptime(user.last_streak, "%Y-%m-%d")
      user.last_mul = datetime.strptime(user.last_mul, "%Y-%m-%d")

      await user.save()
      print(user.last_streak)
