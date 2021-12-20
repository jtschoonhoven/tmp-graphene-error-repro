import graphene
from dataclasses import dataclass
from promise.dataloader import DataLoader
from promise import Promise
from typing import List


@dataclass
class UserModel:
    name: str
    best_friend_id: int
    friend_ids: List[int]


USERS = {
    1: UserModel(name='Alice', best_friend_id=2, friend_ids=[2]),
    2: UserModel(name='Bob', best_friend_id=3, friend_ids=[1, 3]),
    3: UserModel(name='Cass', best_friend_id=4, friend_ids=[1, 2, 4]),
    4: UserModel(name='David', best_friend_id=1, friend_ids=[1, 2, 3]),
}


class UserLoader(DataLoader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.call_count = 0

    def batch_load_fn(self, user_ids: List[int]):
        self.call_count += 1
        return Promise.resolve([USERS[id] for id in user_ids])


user_loader = UserLoader()


class UserObject(graphene.ObjectType):
    name = graphene.String()
    best_friend = graphene.Field(lambda: UserObject)
    friends = graphene.List(lambda: UserObject, first=graphene.Argument(graphene.Int, default_value=5))

    def resolve_best_friend(user: UserModel, *args):
        return user_loader.load(user.best_friend_id)

    def resolve_friends(user: UserModel, *args, first: int = 5):
        friend_ids = user.friend_ids[:first]
        return user_loader.load_many(friend_ids)


class RootQuery(graphene.ObjectType):
    me = graphene.Field(UserObject, required=True)

    @staticmethod
    def resolve_me(root: None, info: graphene.ResolveInfo) -> UserObject:
        return user_loader.load(4)  # type: ignore [no-any-return]


schema = graphene.Schema(query=RootQuery)

friends_query = '''
{
    me {
        name
        bestFriend {
            name
        }
        friends(first: 5) {
            name
            bestFriend {
                name
            }
        }
    }
}
'''
