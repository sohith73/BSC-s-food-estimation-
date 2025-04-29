# VYB AI Assignment: Nutrition Estimation API

#### Overview

This project provides a Flask API that:
     - Accepts a dish name.
          - and checks whether it is a dish or not using LLM 
     - Using my own llm which is fine tuned on lama 1.5B with recipe , costumer interaction , medical data
     - Using LM studio for making api calls between LLM and APi
     - Maps ingredients to a Nutrition Database.

     - Calculates the total nutrition for a standard serving.

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
1. post request with /get_nutrition
2. LLM will see is it a valid dish or any typos are present and return YES or NO as response 
2.1 we use Indexing on the food_name for getting data 
3. then LLM will provide the basic ingredients too with quantities 
4. Calculate the macros of the food 
5. Nutrition Calculation for standard serving size (e.g., 180g).
6. then LLM call is made to see to classify it in which category it falls into 
7. generate a json response 

#### Tech stack used
1. flask - for creating api 
2. LangChain - for LLM interaction
3. LM studio for using my llm as a server 

#### edge cases 
- no matter what our application wont crash 
- used logging for detailed descriptions 
- handles for not dishes and cleverly identifies whether it is a dish or not 
- get more ingredients which are very important 


### using Mock data 
- I created the mock data from the main data main data consist of a lot of things so i reduced for just implementation 

- the files MokResponse.py , MokApiV1.py is a flask with detailed one and the folder with using Mock is also the main implementation 

### what we can improve 
- using redis for most famous recipes 
- we can create recipes database like my fitness-pal , Life-sum this creates the pre made recipes with its nutation facts 
- can create another api for creating dish from scratch - there we can use this data base more 