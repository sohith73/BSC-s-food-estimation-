# BSC FOOD's: Nutrition Estimation API

#### Overview

This project provides a Flask API that:
     - Accepts a dish name.
          - and checks whether it is a dish or not using LLM 
     - Using my own llm which is fine tuned on lama 1.5B with recipe , costumer interaction , medical data
     - Using LM studio for making api calls between LLM and APi
     - Maps ingredients to a Nutrition Database.
     - Calculates the total nutrition for a standard serving.
     - used the best methods as much as possible 
     - main solution in  Using LLM folder

#### Assumptions
Recipe serves 3–4 people by default.

Household measurements mapped to grams:
     
     - 1 cup = 180g
     - 1 tablespoon = 15g
     - 1 teaspoon = 5g

If no direct match is found in Nutrition Database, fuzzy matching is attempted.
If no weight unit is found, fallback to assuming 100g.
Water loss during cooking is ignored.

## provided 2 solutions one is using pure LLM based one and another one is mock data 

### using LLM

#### how it works 
1. post request with `/get_nutrition`  with `{"dish_name": "some name"}`
2. LLM will see is it a valid dish or any typos are present and return YES or NO as response 
2.1 we use Indexing on the food_name for getting data for faster optimized way. don't worry about performance pandas will work very well for the data set it just need around 2 to 5 md of ram 
3. then LLM will provide the basic ingredients too with quantities 
4. Calculate the macros of the food 
5. Nutrition Calculation for standard serving size (e.g., 180g).
6. then LLM call is made to see to classify it in which category it falls into 
7. generate a json response 

#### Tech stack used
1. flask - for creating api 
2. LangChain - for LLM interaction
3. LM studio for using my llm as a server 
4. pandas for csv handing and indexing for fast search

#### edge cases 
- no matter what our application wont crash under any scenario
- used logging for detailed descriptions 
- handles for not dishes and cleverly identifies whether it is a dish or not 
- get more ingredients which are very important 
- * it will also work for the dishes which are not present in csv, added a new column 

```
"source": "csv" or "source": "llm"
```


### using Mock data 
- I created the mock data from the main data main data consist of a lot of things so i reduced for just implementation 

- the files MokResponse.py , MokApiV1.py is a flask with detailed one and the folder with using Mock is also the main implementation 

### what we can improve 
- using redis for most famous recipes 
- we can create recipes database like my fitness-pal , Life-sum this creates the pre made recipes with its nutation facts 
- can create another api for creating dish from scratch - there we can use this data base more 


## blue print 

```
Start
 |
 |--> 1. Take Dish Name Input
 |
 |--> 2. Validate/Spell-Check Dish Name using LLM
 |        |
 |        |---> If Not a Dish --> Return Error
 |        |
 |        |---> If Valid Dish --> Continue
 |
 |--> 3. Search Dish in Nutrition Database
 |        |
 |        |---> If Found --> Return Nutrition value and continue from Database in index of food_name 
 |        |
 |        |---> If Not Found --> Continue
 |
 |--> 4. Ask LLM to Fetch Generic Recipe (ingredients + quantities)
 |
 |--> 5. Parse Ingredients List
 |
 |--> 6. Standardize Units to (cup, tsp, katori, etc.)
 |
 |--> 7. Convert Quantities to Grams
 |
 |--> 8. Map Ingredients to Nutrition Database (handle spelling errors)
 |
 |--> 9. Calculate Total Nutrition
 |
 |--> 10. Identify Dish Type (Wet Sabzi, Dal, etc.)
 |
 |--> 11. Extrapolate Nutrition for Standard Serving (e.g., 180g)
 |
 |--> 12. Return Final JSON Output
 |
End

```

## images of Api testing from LLM approach.
![Screenshot (555)](https://github.com/user-attachments/assets/68272b4d-1728-44ba-aa00-82d8a48107b2)
1. **Handling Non-Food Items:** If the input is not recognized as a food item, the system will respond with "This is not a food item. Please try again."

![Screenshot (553)](https://github.com/user-attachments/assets/9bbf81af-8b5e-49b9-8a98-13f5ce1bf65e)

![Screenshot (551)](https://github.com/user-attachments/assets/89c4e4e1-3554-448f-bc45-1968a788c4b2)

![Screenshot (550)](https://github.com/user-attachments/assets/8435f674-f5e9-447a-9e20-e16fa13150c6)
- dish created  by LLm it self
   ![Screenshot (546)](https://github.com/user-attachments/assets/afa57032-80b1-4395-bd3f-38f55d2954a3)
- dish from data base(csv)
- ![Screenshot (548)](https://github.com/user-attachments/assets/fad6f044-ad39-4d03-8dfb-867bc46e16a3)

- 
