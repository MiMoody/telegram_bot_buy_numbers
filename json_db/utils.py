import json
from pathlib import Path
import os
pwd = Path(__file__).parent

class JsonStruct:
    
    @classmethod
    def get(cls, name_table:str):
        with open(os.path.join(pwd, f"{name_table}.json"), "r"  ) as f:
            file = json.load(f)
        return file
    
    @classmethod
    def save(cls, name_table:str, data:dict):
        with open(os.path.join(pwd, f"{name_table}.json"), "w+" ) as f:
            json.dump(data, f, ensure_ascii=False)
    