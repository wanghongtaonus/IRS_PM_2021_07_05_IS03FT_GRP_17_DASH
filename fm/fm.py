import os
import pandas as pd


#reload db
def update_db(rt_file_path = "../rt/"):
    #print(os.getcwd())
    #print(rt_file_path + "runtime.csv")
    if(os.path.exists(rt_file_path + "runtime.csv") == True):
        df = pd.read_csv(rt_file_path + "runtime.csv")
        #print("read succ")
        return df
    else:
        print("no exiting file")
        return -1
   
def save_db(input_data,rt_file_path = "../rt/"):
    input_data.to_csv(rt_file_path + "runtime.csv", index = False)
#os.path.exists(test_file.txt)
#input: id
#output: list
#id: users' id number
#list: row in file
def search_by_id(id_number):
    db = update_db()
    index = db[db.id == id_number].index.tolist()[0]
    temp = db.loc[index].to_dict()
    return temp
    
    
    
def search_by_name(name):
    db = update_db()
    index = db[db.name == name].index.tolist()
    temp = []
    if(len(index) == 0):
        return temp
    for i in index:
        print(i)
        temp.append(db.loc[i].to_dict())
    return temp
    
  
def edit_row(input_data):
    db = update_db()
    id_number = input_data["id"]
    index = db[db.id == id_number].index.tolist()[0]
    #print(index)
    for i in db.columns:
        #print(index, i)
        db.loc[db.index == index, i] = input_data[i]
    save_db(db)
    return
    
def add_row(input_data):
    db = update_db()
    db = db.append(input_data, ignore_index=True)
    #print(index)
    save_db(db)
    return
    
def del_row(id_number):
    db = update_db()
    db = db.drop(db[db.id == id_number].index)
    #print(index)
    save_db(db)
    return
    
def show(rt_file_path = "../rt/"):
    db = update_db(rt_file_path)
    print(db)
    