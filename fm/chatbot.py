from flask import Flask, Response, request
import json
import threading,time
from fm import *
from init_data import *
sys.path.append("../model")
sys.path.append("../um")
from md import *
from main import *
'''
def wait_lock(lock):
    lock_path = "../rt/lock"
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


def rel_lock(lock): 
    lock_path = "../rt/lock"
    #print("release lock")
    os.remove(lock_path)
'''

lock = threading.Lock()
app = Flask(__name__)
id_default = 0


@app.route("/", methods = ["POST"])
def chatbot_main():
    global cond
    global resp
    global parts_list
    global syms_list
    req = request.get_json(silent=True, force=True)
    print(req)
    intent_name = req["queryResult"]["intent"]["displayName"]
    cond.acquire()
    if intent_name == "illness":
        parts_list = req["queryResult"]["parameters"]["parts_main"]
        syms_list = req["queryResult"]["parameters"]["symptom"]
        #print("11111")
        cond.notify()
        #print("22222")
        cond.wait()
        #print(resp)
        resp_text = resp
    elif(intent_name == "des"):
        resp = req["queryResult"]["parameters"]["decision"]
        print("11111")
        cond.notify()
        print("22222")
        cond.wait()
        print(resp)
        resp_text = resp
    else:
        resp_text = "Unable to find a matching intent. Try again."
    resp = {
        "fulfillmentText": resp_text
    }
    cond.release()
    return Response(json.dumps(resp), status=200, content_type="application/json")

def run_chatbot():
    app.run(host='0.0.0.0', port=5000, debug=True)

def find_nextq(idx):
    wait_lock(lock)
    db = update_db()
    nextq = ""
    ok = 0
    for col in db.columns:
        if(db.loc[idx, col] == 4):
            nextq = col
            ok = 1
            break
    save_db(db)
    rel_lock(lock)
    return nextq,ok

def change_row(idx, typ, val):
    wait_lock(lock)
    db = update_db()
    db.loc[idx, typ] = val
    save_db(db)
    rel_lock(lock)

def detect_owner(idx):
    ok = 0
    wait_lock(lock)
    db = update_db()
    if(db.loc[idx, "owner"] == 0):
        ok = 1
    save_db(db)
    rel_lock(lock)
    return ok

def wait_get_nextq(tt_symptom, id_default, mode): #mode=1 asked_yes mode = 2 asked_no
    if(mode == 1):
        change_row(id_default, tt_symptom, 3)
    elif(mode == 2):
        change_row(id_default, tt_symptom, 2)
    change_row(id_default, "next_question", 1)
    change_row(id_default, "owner", 1)
    while(detect_owner(id_default) == 0):
        pass
    nextq,ok = find_nextq(id_default)
    return nextq,ok

def generate_sentence(symptom, sym_list):
    for sym in sym_list:
        if(sym.symptom == symptom):
            break
    if(sym.part_num == 0 and sym.sym_num == 1):
        return 'Do you have {}'.format(sym.syms[0])
    elif(sym.part_num == 1 and sym.sym_num == 1):
        return 'Do you have {} in your {}'.format(sym.syms[0], sym.parts[0])
    elif(sym.part_num == 2 and sym.sym_num == 1):
        return 'Do you feel {} in your {} and {}'.format(sym.syms[0], sym.parts[0], sym.parts[1])
    elif(sym.part_num == 1 and sym.sym_num == 2):
        return 'Do you have {} {} {}'.format(sym.syms[1], sym.parts[0], sym.syms[0])
    else:
        return "Please say it again."

def main():
    global cond
    global resp
    global parts_list
    global syms_list
    global id_default
    global sym_list
    global all_sym_list
    global all_part_list
    while 1:    #root loop
        id_default += 1
        cond.acquire()
        cond.wait()
        print("step 1")
        while 1:   #step 1: patients describe
            c_list = sym_list
            if(len(parts_list) > 0):
                for i in parts_list:
                    if( i in all_part_list):
                        temp_list = sym_filter(c_list, i, 1)
                        if(len(temp_list) >= 1):
                            c_list = temp_list
            if(len(syms_list) > 0):
                for i in syms_list:
                    if(i in all_sym_list):
                        temp_list = sym_filter(c_list, i, 2)
                        if(len(temp_list) >= 1):
                            c_list = temp_list
            resp = "Is there anything else you feel uncomfortable with?"
            print("ttttttt")
            cond.notify()
            print("sssssss")
            cond.wait()
            print(resp)
            if(resp == "no"):
                break
        
        p_count = 0
        s_count = 0
        print("step 2")
        while(len(c_list) > 1):#check if the first symptom is complete
            out_parts,out_syms = find_next(c_list)
            temp = ""
            typ = 0
            if(len(out_parts) > 0):
                resp = "Do you feel bad in " + out_parts[p_count]
                p_count += 1
                temp = out_parts[p_count]
                typ = 1
            elif(len(out_syms) > 0):
                resp = "Is it {}?".format(out_syms[s_count])
                temp = out_syms[s_count]
                s_count += 1
                typ = 2
            cond.notify()
            cond.wait()
            if(resp == "no"):
                continue
            if(resp == "yes"):
                temp_list = sym_filter(c_list, temp, typ)
                if(len(temp_list) >= 1):
                    c_list = temp_list
        print("step 3")
        tt_symptom = c_list[0].symptom
        next_question,ok = wait_get_nextq(tt_symptom, id_default, 1)
        print("here 172")
        if(ok == 1):
            resp = generate_sentence(next_question, sym_list)
            cond.notify()
            cond.wait()
        elif(ok == 0):
            resp = "That's all, thank you."
            cond.notify()
            cond.release()
            continue
        
        while 1:
            if(resp == "yes"):
                next_question,ok = wait_get_nextq(next_question, id_default, 1)
                if(ok == 1):
                    resp = generate_sentence(next_question, sym_list)
                    cond.notify()
                    cond.wait()
                elif(ok == 0):
                    resp = "That's all, thank you."
                    cond.notify()
                    break
            elif(resp == "no"):
                next_question,ok = wait_get_nextq(next_question, id_default, 2)
                if(ok == 1):
                    resp = generate_sentence(next_question, sym_list)
                    cond.notify()
                    cond.wait()
                elif(ok == 0):
                    resp = "That's all, thank you."
                    cond.notify()
                    break  
        cond.release()
        
def um_process():
    global lock
    print("um_main in !!!!")
    while 1:
        ok = um_main(lock)
        if(ok == 0):
            break

parts_list = []
syms_list = []
resp = ""
db = update_db()
print("iiiiiiiiiiii")
sym_list, all_sym_list, all_part_list = Init_all()
cond = threading.Condition()
t_main = threading.Thread(target=main)
print("t_main start")
um = threading.Thread(target=um_process)
print("um start")
t_main.start()
um.start()
run_chatbot()
t_main.join()
um.start()