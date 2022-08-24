

class DbExecutor:
    """ Класс позволяет выполнять sql запросы """
    
    def __init__(self, connector):
        """ На вход получает DbConnector """
        
        self.__connector = connector
        self.__cursor_result = None
        
    def __await__(self):
        return self._async_init().__await__()

    async def _async_init(self):
        self.__cursor = await self.__connector.cursor()
        return self
    
    async def execute(self, query:str, *args):
        """ Метод выполняет запрос"""
        
        await self.__cursor.execute(query, *args)
        try:
            self.__cursor_result = await self.__cursor.fetchall()
        except:
           self.__cursor_result = None 
    
    def get_dict_result(self):
        """ Метод преобразует данные от базы в словарь"""
        
        if not self.__cursor_result:
            raise Exception("You should be execute query!")
        return self.__dictfetchall()
    
    def get_raw_result(self):
        """Получает сырой результат от бд, без столбцов"""
        return self.__cursor_result

    def __dictfetchall(self) -> list:
        """Преобразует строки, полученные от бд в формат словаря"""

        desc = self.__cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in self.__cursor_result
        ]

    async def close(self):
        await self.__connector.close()