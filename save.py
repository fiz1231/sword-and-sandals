import pickle
import time
#class resposible for saving and loading players and enemy data to the game
class saves():
    def __init__(self):
        self.saved=[]
    def save(self):
        if saves!=[]:

            with  open("save.data",'wb') as file:
                pickle.dump(self.saved,file)
        else:
            return 0

    def load(self):
        try:

            with open("save.data",'rb') as s:
                self.saved=pickle.load(s)

            return self.saved
        except(FileNotFoundError):
            pass
    def add(self,save_stats):
        self.saved.append([save_stats,time.ctime(time.time())])
