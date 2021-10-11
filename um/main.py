import sys
import fm
import os
import time
import md
import pandas as pd
import threading

def wait_lock(lock):
    lock.acquire()



def rel_lock(lock): 
    lock.release()
    

def um_main(lock):
    wait_lock(lock)
    db = fm.update_db()
    t_list = db.loc[db.owner == 1]
    if(len(t_list) > 0):
        print("detect owner == 1")
        for temp in t_list.iterrows():
            idx = temp[0]
            illness = temp[1]["illness"]
            akd_yes = []
            akd_no  = []
            for i in db.columns:
                if(i == "id" or i == "name" or i == "illness" or i == "therapy" or i == "report" or i == "owner" or i == "next_question"):
                    continue
                else:
                    if(temp[1][i] == 3):
                        akd_yes.append(i)
                    elif(temp[1][i] == 2):
                        akd_no.append(i)
            if(temp[1]["next_question"] == 1):
                nxt_qutin,illness = md.get_nextquestion(akd_yes, akd_no)
                if(len(nxt_qutin) > 0):
                    db.loc[idx, nxt_qutin] = 4
                db.loc[idx, "next_question"] = 0
                db.loc[idx, "illness"] = illness

            if(temp[1]["therapy"] == 1):
                thrpy = md.get_therapy(akd_yes, illness)
                db.loc[idx, "therapy"] = thrpy
                
            if(temp[1]["report"] == 1):
                md.mk_report(temp[1])
                db.loc[idx, "report"] = 0
            db.loc[idx, "owner"] = 0
            fm.save_db(db)
    rel_lock(lock)

'''
if __name__ == "__main__":
    # execute only if run as a script
    while 1:
        um_main()

'''