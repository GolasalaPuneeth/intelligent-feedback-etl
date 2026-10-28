from ValidationLayer import FeedbackHookValidation
from Apputils import hasher
from DatabaseLayer import Irepo,Repo
from CeleryLayer import test_task

repo : Irepo = Repo()

class FeedBackProcessor:
    
    async def ProcessFeedBack(self,data:FeedbackHookValidation):
        hash = hasher.get_hash(data)
        # print("[SERVICE]->",hash)
        if repo.check_record_persist(hash):
            # print("[SERVICE]","Found")
            return {"FOUND":True}
        res = test_task.delay(data.model_dump(),hash)
        return res.id
#sample data

# {
#   "source_id": "TICK-99482",
#   "channel": "zendesk_webhook",
#   "raw_text": "URGENT! My payment failed for subscription ID 4481. My name is John Doe, call me at 555-0199 or john@example.com ASAP! Fix this app crash!"
# }