from ValidationLayer import FeedbackHookValidation
from Apputils import hasher

class FeedBackProcessor:
    def FeedbackChecker(self,data_hash):
        print("from FeedBack Checker",data_hash)
        return data_hash
    
    def ProcessFeedBack(self,data:FeedbackHookValidation):
        hash = hasher.get_hash(data)
        self.FeedbackChecker(hash)
        return hash