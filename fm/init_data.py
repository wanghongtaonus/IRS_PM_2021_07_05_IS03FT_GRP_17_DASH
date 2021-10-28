import os
import sys
from fm import *


class sym_Node:
    def __init__(self, symptom, part_num, parts, sym_num, syms):
        self.part_num = part_num
        self.parts = parts
        self.sym_num  = sym_num
        self.syms = syms
        self.symptom = symptom
        self.info = [symptom, part_num, parts, sym_num, syms]


def Init_row(num = 10):
    db = update_db()
    for idx in range(num):
        temp = search_by_id(idx + 1)
        for i in db.columns:
            temp[i] = 0
        temp["id"] = idx + 1
        temp["name"] = "Joe"
        edit_row(temp)
    return





def Init_all():
    Init_row()                      #init row 1 
    f = open("symptoms.txt","r")   #获取文件对象
    line = f.readline()
    all_sym_list = {}
    all_part_list = {}
    sym_count = 0
    part_count = 0
    sym_list = []
    while line:
        line = line.replace('\n', '')
        temp = line.split(" ")
        part_num = 0
        parts = []
        sym_num = 0
        syms = []
        symptom = ""
        if(temp[1] != '0'):
            part_num += 1
            parts.append(temp[1])
            if(temp[1] not in all_part_list.keys()):
                all_part_list[temp[1]] = part_count
                part_count += 1
        if(temp[2] != '0'):
            part_num += 1
            parts.append(temp[2])
            if(temp[2] not in all_part_list.keys()):
                all_part_list[temp[2]] = part_count
                part_count += 1
        if(temp[3] != '0'):
            sym_num += 1
            syms.append(temp[3])
            if(temp[3] not in all_sym_list.keys()):
                all_sym_list[temp[3]] = sym_count
                sym_count += 1
        if(temp[4] != '0'):
            sym_num += 1
            syms.append(temp[4])
            if(temp[4] not in all_sym_list.keys()):
                all_sym_list[temp[4]] = sym_count
                sym_count += 1
        symptom = temp[0]
        temp_node = sym_Node(symptom, part_num, parts, sym_num, syms)
        sym_list.append(temp_node)
        #print(temp_node.info)
        line = f.readline()  #读取一行文件，包括换行符

    #print(sym_list)
    f.close() #关闭文件
    return sym_list, all_sym_list, all_part_list
    

#filter
def sym_filter(sym_list, data_in, data_typ):
    out_list = []
    for item in sym_list:
        if(data_typ == 1):
            if(data_in in item.parts):
                out_list.append(item)
        elif(data_typ == 2):
            if(data_in in item.syms):
                out_list.append(item)
    return out_list

#filter
def sym_filter_no(sym_list, data_in, data_typ):
    out_list = []
    for item in sym_list:
        if(data_typ == 1):
            if(data_in not in item.parts):
                out_list.append(item)
        elif(data_typ == 2):
            if(data_in not in item.syms):
                out_list.append(item)
    return out_list

def find_next(out_list):
    l = len(out_list)
    p_dict = {}
    s_dict = {}
    for out in out_list:
        for part in out.parts:
            if(part not in p_dict):
                p_dict[part] = 0
            else:
                p_dict[part] += 1
        for sym in out.syms:
            if(sym not in s_dict):
                s_dict[sym] = 0
            else:
                s_dict[sym] += 1
    out_parts = []
    out_syms = []
    for key in p_dict:
        if(p_dict[key] == l - 1):
            continue
        else:
            out_parts.append(key)
    for key in s_dict:
        if(s_dict[key] == l - 1):
            continue
        else:
            out_syms.append(key)
    return out_parts,out_syms



#opening_Q&A
'''
def op_QA(data_in, sym_list)
    data_typ = 0 # 1 part 2 sym
    sym_list, all_sym_list, all_part_list = Init_all()
    if(data_in in all_part_list):
        data_typ = 1
    if(data_in in all_sym_list):
        data_typ = 2
    if(data_typ != 0):
        out_list = sym_filter(sym_list, data_in, data_typ)
        out_parts,out_syms = find_next(out_list)
    if(len(out_parts) > 0):
        return 1,out_list
    elif(len(out_syms) > 0):
        return 2,out_list
    return 0,out_list   
'''