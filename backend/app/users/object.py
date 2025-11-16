from models.models import User

from users.requests import user_repo


class UserObj:
    def __init__(self, user: User, data: dict):
        self.user = user # user object
        self.data = data

    @classmethod
    async def init_object(cls, name):
        # init object user, create data dict
        # return user and data in object
        user = await user_repo.get_by_name(name)

        data = {
                "name": user.name,
                "level": user.level,
                "xp": user.xp,
                "Spoints": user.Spoints,
                "days_streak": user.days_streak,
                "mul": user.mul,
                "sale_shop": user.sale_shop,
                "last_streak": user.last_streak.timestamp(),
                "last_mul": user.last_mul.timestamp(),
                "complete_simple_tasks": user.complete_simple_tasks,
                "complete_common_tasks": user.complete_common_tasks,
                "complete_hard_tasks": user.complete_hard_tasks,
                "complete_expert_tasks": user.complete_expert_tasks,
                "complete_hardcore_tasks": user.complete_hardcore_tasks,
        }
        
        return cls(user, data)

