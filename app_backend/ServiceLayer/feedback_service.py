from ValidationLayer import FeedbackHookValidation
from Apputils import hasher
from DatabaseLayer import Irepo,Repo

repo : Irepo = Repo()

class FeedBackProcessor:
    
    async def ProcessFeedBack(self,data:FeedbackHookValidation):
        hash = hasher.get_hash(data)
        print("[SERVICE]->",hash)
        if repo.check_record_persist(hash):
            print("[SERVICE]","Found")
            return None
        # await self.FeedbackChecker(hash)
        # return hash