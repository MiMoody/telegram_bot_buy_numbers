import aiopg


class DbConnector:
    """ Класс возвращает обьект aiopg connecto для подключения к бд """
    
    @catch_exception
    def  __init__(self,):
        self.__database= DB["database"]
        self.__user = DB["user"]
        self.__password = DB["password"]
        self.__host = DB["host"]
        
    @catch_exception
    def __await__(self):
        return self._async_init().__await__()
    
    @catch_exception
    async def _async_init(self):
        self.__conn = await aiopg.connect(
                               database=self.__database,
                               user=self.__user,
                               password=self.__password,
                               host=self.__host)
        return self.__conn