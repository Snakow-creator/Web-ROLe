from models.models import User

from datetime import datetime

async def str_to_datetime():
    for user in await User.find().to_list():
      if type(user.last_mul) == str:
          last_mul = user.last_mul
      else:
          last_mul = user.last_mul.strftime("%Y-%m-%d")

      if type(user.last_streak) == str:
          last_streak = user.last_streak
      else:
          last_streak = user.last_streak.strftime("%Y-%m-%d")

      user.last_streak = datetime.strptime(last_streak, "%Y-%m-%d")
      user.last_mul = datetime.strptime(last_mul, "%Y-%m-%d")

      await user.save()
      print(user.last_streak)
