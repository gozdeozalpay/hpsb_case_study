import json
import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from flask import Flask
import pickle
import warnings
import logging
from time import time
import uvicorn
from fastapi import FastAPI
from Request import request


warnings.filterwarnings('ignore')

logging.getLogger().setLevel(logging.INFO)

recommender = FastAPI()

@recommender.post('/predict')

#async def create_item(request: request):
#    return request

def predict(data:request):

    data=data.dict()
    item= data['product_name']

    with open('events.json','r') as f:
        events = json.loads(f.read())
    events_data = pd.json_normalize(events, record_path =['events'])

    with open('meta.json','r') as f:
        meta = json.loads(f.read())
    meta_data= pd.json_normalize(meta, record_path =['meta'])

    def preProcessing(data):
        #Productid alanı null olan satırlar elendi. 
        data=data[data['productid'].notna()]
        data['Quantity']=1
        data_v1=data[['sessionid', 'name', 'Quantity']].drop_duplicates()
        return data, data_v1

    def basket(data):
        basket_data = data.groupby(['sessionid', 'name'])['Quantity']\
                            .sum().unstack()\
                            .reset_index().fillna(0)\
                            .set_index("sessionid")
        return basket_data

    def mostfrequentProducts(data):
        product_counts=data.groupby(['name', 'subcategory'])['Quantity'].sum()
        product_counts=pd.DataFrame(product_counts, columns=['Quantity']).reset_index().sort_values(by='Quantity', ascending=False)
        
        product_counts['count_max'] = product_counts.groupby(['subcategory'])['Quantity'].transform(max)
        most_frequent_products=product_counts[product_counts['Quantity']==product_counts['count_max']].drop('count_max', axis=1)
        return most_frequent_products


    def frequently_bought_t(data, n_of_items):
        if item_d.shape[0]>35:
            # Applying apriori algorithm on item df
            frequentitemsets = apriori(item_d, min_support=0.003, use_colnames=True)
            # Storing association rules
            rules = association_rules(frequentitemsets, metric="lift", min_threshold=1)
            # Sorting on lift and support
            rules.sort_values(['lift','support'],ascending=False).reset_index(drop=True)
            # Returning top 10 items with highest lift and support 
            suggestion = rules['consequents'].unique()[:n_of_items+1]
            suggestions=pd.DataFrame(suggestion, columns=['suggestion'])
            suggestions['suggestion'] = suggestions['suggestion'].apply(set)
            suggestions['suggestion'] = suggestions['suggestion'].str.join(', ')
            suggestions_list=suggestions['suggestion'].to_list()
            return suggestions_list
        else:
            products_list=most_frequent_products.head(n_of_items)
            most_frequent_product_list=products_list['name'].to_list()
            most_frequent_product_list.insert(0, item)
            return most_frequent_product_list

    def all_suggestions(suggestion, n_of_items): 
        number_of_products=(n_of_items+1)-len(suggestions_list)
        if len(suggestions_list) == (n_of_items):
            return suggestions_list
        else:
            added_products_list=most_frequent_products.query("name not in @suggestions_list").head(number_of_products)['name'].tolist()
            all_suggestions=(suggestions_list+added_products_list)[1:]
            return all_suggestions



    data=pd.merge(events_data, meta_data, on='productid', how='left')
   
    logging.info("Preprocessing...")
    data, data_v1=preProcessing(data)
    logging.info("Preprocessing is done.")

    logging.info("Basket data is created for algorithm...")
    basket_data=basket(data_v1)
    
    
    logging.info("Most frequent 10 products are selected  ...")
    most_frequent_products=mostfrequentProducts(data)
     
    item_d = basket_data.loc[basket_data[item]==1]

    n_of_items=10

    if item_d.shape[0]>35:
        # Applying apriori algorithm on item df
        frequentitemsets = apriori(item_d, min_support=0.003, use_colnames=True)
        # Storing association rules
        rules = association_rules(frequentitemsets, metric="lift", min_threshold=1)
        # Sorting on lift and support
        rules.sort_values(['lift','support'],ascending=False).reset_index(drop=True)
        # Returning top 10 items with highest lift and support 
        suggestion = rules['consequents'].unique()[:n_of_items+1]
        suggestions=pd.DataFrame(suggestion, columns=['suggestion'])
        suggestions['suggestion'] = suggestions['suggestion'].apply(set)
        suggestions['suggestion'] = suggestions['suggestion'].str.join(', ')
        suggestions_list=suggestions['suggestion'].to_list()
    else:
        products_list=most_frequent_products.head(n_of_items)
        most_frequent_product_list=products_list['name'].to_list()
        most_frequent_product_list.insert(0, item)

    
    recommendations_all=all_suggestions(suggestions_list, 10)


    recommendations = json.dumps(recommendations_all, ensure_ascii=False, indent=2).encode('utf8')

    return  {'Recommendations for this product: ', recommendations.decode()}

#uvicorn recommender:recommender --reload




