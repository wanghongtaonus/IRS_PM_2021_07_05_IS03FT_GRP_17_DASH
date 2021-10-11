import sys
import os
import pandas as pd
sys.path.append("./fm")
sys.path.append("./model")
import fm
import time


def wait_lock():
    lock_path = "./rt/lock"
    while 1:
        #wait forever
        time.sleep(0.2)
        if(os.path.exists(lock_path) == False):
            open(lock_path, 'wb')
            #print("get lock")
            break;
        else:
            #print("sleep")
            pass

def rel_lock():
    lock_path = "./rt/lock"
    #print("release lock")
    os.remove(lock_path)


def change_row(idx, typ, val):
    wait_lock()
    db = fm.update_db("./rt/")
    db.loc[idx, typ] = val
    fm.save_db(db,"./rt/")
    fm.show("./rt/")
    rel_lock()


def show():
    fm.show("./rt/")


show()
change_row(0, "owner", 1)