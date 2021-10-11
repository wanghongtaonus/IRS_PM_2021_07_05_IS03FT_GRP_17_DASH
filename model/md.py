import sys
import os
from IRS_utils import *


def get_nextquestion(akd_yes, akd_no):
    nxt_question,illness = NextQuestion(akd_yes,akd_no)
    print("next is " + nxt_question)
    print("#### out ####")
    return nxt_question,illness
    
def get_illness(akd_yes):
    print("#### get_illness function####")
    print(akd_yes)
    illness = 3
    print("illness is %d"%illness)
    print("#### out ####")
    return illness
    
def get_therapy(akd_yes, illness):
    print("#### get_therapy function####")
    print(akd_yes, illness)
    therapy = 3
    print("therapy is %d"%therapy)
    print("#### out ####")
    return therapy
    
    
def mk_report(info):
    print("#### mk_report function####")
    print(info)
    print("#### out ####")
    return
    