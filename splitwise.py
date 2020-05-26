import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import time

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


# key maximum
def max_dict_key(my_dict):
    return max(my_dict, key=my_dict.get)

#key minimum
def min_dict_key(my_dict):
    return min(my_dict, key=my_dict.get)

#value max
def max_dict_value(my_dict):
    maximum = max(my_dict, key=my_dict.get)
    return my_dict[maximum]

#value min
def min_dict_value(my_dict):
    maximum = min(my_dict, key=my_dict.get) 
    return my_dict[maximum]

def closer_to_zero(my_dict):

    owes_owed = min_dict_value(my_dict) + max_dict_value(my_dict)
    ans = max_dict_value(my_dict) + min_dict_value(my_dict)
    lsts = []
    if ans >0:
        lsts.append(str(min_dict_key(my_dict))  + " pays " + str(round(abs(min_dict_value(my_dict)), 2)) + " to " +  str(max_dict_key(my_dict)) + ', ')
        replace_value_with_definition(my_dict, min_dict_key(my_dict), 0)
        replace_value_with_definition(my_dict, max_dict_key(my_dict), owes_owed)

    else:
        lsts.append(str(min_dict_key(my_dict))  + " pays " + str(round(max_dict_value(my_dict),2))+ " to "  +  str(max_dict_key(my_dict)) + ', ' )
        replace_value_with_definition(my_dict, min_dict_key(my_dict), owes_owed)
        replace_value_with_definition(my_dict, max_dict_key(my_dict), 0)
    return lsts

#function to replace values in dict
def replace_value_with_definition(my_dict, key_to_find, definition):
    for key in my_dict.keys():
        if key == key_to_find:
            my_dict[key] = definition

def Convert(lst): 
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)} 
    return res_dct 


@app.route('/splitwise/<my_dict>', methods = ['GET'])
@cross_origin()
def splitwise(my_dict):
   
    my_dict = my_dict.split(",")

    my_dict = Convert(my_dict)
    my_dict = [dict([a, int(x)] for a, x in b.items()) for b in [my_dict]][0]

    #find out average amount
    average_amount_spent = (sum(my_dict.values())) / len(my_dict)

    #now take off average_amount_spent from each amount spent in the dict
    for key in my_dict:    
        my_dict[key] =  my_dict[key] - average_amount_spent

    ## find out difference of payment from top debter and creditor
    owes_owed = min_dict_value(my_dict) + max_dict_value(my_dict)
            
    # create a while loop which will equal out creditor/debtor
    lsts=[]
    while max_dict_value(my_dict) != 0:
        lsts.append(closer_to_zero(my_dict))


    lsts = [{"payees":  lsts }]
    return jsonify({"pay":lsts})
    

if __name__ == "__main__":
    app.run(debug=True)
