import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import time

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Functions _____________
def Word_Search(x):
    df[x] = df['Ingredients'].str.contains(x, flags=re.IGNORECASE)
    df[x] = df[x].replace(True, 1)
    df[x] = df[x].replace(False, 0)
    return 

def ingredients_in(list_of_ingredients_in):
    [Word_Search(ingred) for ingred in list_of_ingredients_in]
    return

def split(x):
    if len(x) == 1:
        return x[0]
    else:
        return x.split(',')

def Check_if_in(df):
    ingredients = [df.Ingredients.count(x) for x in df.Ingredients_inn_split]
    ingredients = [1 if i >=1 else i for i in ingredients]
    return sum(ingredients)

# Functions END _____________

@app.route('/')
def hello_world():
    """Print 'Hello, world!' as the response body."""
    return 'Hello, world!'
    

@app.route('/recipes', defaults ={'ingreds': "onions, chicken, pasta"})
@app.route('/recipes/<ingreds>', methods = ['GET'])
@cross_origin()
def recipes(ingreds):
    #text = request.get_json()
    #text = {"ingred":"onions, chicken, pasta"}
    text = {"ingreds":ingreds}

    df = pd.read_csv('JAMIE_MOB_BBC_29_04_2020.csv', encoding= 'unicode_escape')
    df = df.replace(np.nan, '')
    df['Ingredients_inn'] = str(text['ingreds'])
    df['Ingredients'] = df['Ingredients'].str.lower()
    df['Ingredients_inn_split'] = df['Ingredients_inn'].apply(split)
    df = df.assign(Matching_ingred=df.apply(Check_if_in, axis = 1))
    df['Ingredients_to_buy'] = df['Number of ingredients'] - df['Matching_ingred']
    df1 = df[df['Matching_ingred'] > 0]
    df1 = df1[df1['Number of ingredients'] > 0]
    df1 = df1.sort_values(['Matching_ingred', 'Ingredients_to_buy'], ascending=[False, True])
    
    df1 = df1[['cuisine', 'Title', 'Ingredients', 'Link', 'Matching_ingred', 'Ingredients_to_buy', 'Image_link']]

    #titles = df1['Title'].tolist()
    #return jsonify({'Titles' : titles})
    Recipes  = df1.to_dict('records')
    ex1 = jsonify({'Recipes' : Recipes})
    return ex1


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

tt = [
    {
      "cuisine": "Indian"  }
  ]

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
    

 #Recipes  = df1.to_dict('records')
    #ex1 = jsonify({'Recipes' : Recipes})
    #return ex1



    

if __name__ == "__main__":
    app.run(debug=True)