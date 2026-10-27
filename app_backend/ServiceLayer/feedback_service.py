from ValidationLayer import FeedbackHookValidation
from Apputils import hasher
from DatabaseLayer import Irepo,Repo

repo : Irepo = Repo

class FeedBackProcessor:
    async def FeedbackChecker(self,data_hash):
        print("from FeedBack Checker",data_hash)
        return data_hash
    
    async def ProcessFeedBack(self,data:FeedbackHookValidation):
        hash = hasher.get_hash(data)
        await self.FeedbackChecker(hash)
        return hash