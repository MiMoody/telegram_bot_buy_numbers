import sys
sys.path.append("../")
from json_db.utils import JsonStruct


class User:
    
    @classmethod
    def create(cls, user_id:int, **kwargs):
        users = JsonStruct.get("user")
        if user_id in users:
            raise Exception("User alreasy exist!")
        users[user_id] = kwargs
        JsonStruct.save("user", users)
    
    @classmethod
    def get_by_id(cls, user_id:str):
        users = JsonStruct.get("user")
        return users.get(user_id)
