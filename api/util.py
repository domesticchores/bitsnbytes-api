import json

def format_return_msg(msg):
    format = '''{
                'message': {msg}
            }'''
    return format

def open_food_data():
    with open("test_food_data.json") as my_file:
        data = json.load(my_file)
        #labelNutrients = (data['labelNutrients']['fat']['value'])
        #print(labelNutrients)

        #print(data['foodNutrients'][0]['amount'])

        name_list = {
            "Fatty acids, total saturated":"Saturated Fat"
            
        }

        #fiber_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][0]['amount']))
        #Iron_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][1]['amount']))
       # Potassium_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][2]['amount']))
        #Cholestral_amount = print((data['foodNutrients'][3]['nutrient']['name']) + " " +(data['servingSize']) / 100 * (data['foodNutrients'][3]['amount']))
        #Calcim_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][4]['amount']))
        #total_sugars_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][5]['amount']))
       # sodium_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][6]['amount']))
        #protein_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][7]['amount']))
        #sugars_added_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][8]['amount']))
        #trans_Fat_amount = print((data['servingSize']) / 100 * (data['foodNutrients'][9]['amount']))
        saturated_Fat_amount = print(name_list[(data['foodNutrients'][10]['nutrient']['name'])], (data['servingSize']) / 100 * (data['foodNutrients'][10]['amount']))
        
        print(saturated_Fat_amount)



        #print(data['foodNutrients'][0]['nutrient'])
        #for foodNutrient in data['foodNutrients']:
            #print(foodNutrient['type'])
            
            
            #print(data['labelNutrients'][item]['value'])
        
def main():
    open_food_data()
main()