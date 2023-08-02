#!/usr/bin/env python
# coding: utf-8

# In[95]:


import pandas as pd


# In[96]:


import requests


# In[97]:


# Send a GET request to a website and get the response
response = requests.get('https://www.example.com')


# In[98]:


# Check the content of the response (HTML content in this case)
print("Content:", response.text)


# In[ ]:





# In[99]:


response.status_code


# In[100]:


response.content


# In[101]:


response.headers


# In[102]:


response.headers['Content-Type']


# In[191]:


response1 = requests.get('https://globalmart-api.onrender.com/mentorskool/v1/sale')


# In[192]:


response1.status_code


# In[193]:


response1.headers['Content-Type']


# In[194]:


url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
headers = {
    'accept': 'application/json',
    'access_token': 'fe66583bfe5185048c66571293e0d358'
}

 

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for any HTTP errors
    data = response.json()

 

    # Process and work with the data here
    print(data)

 

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")


# In[299]:


# Fetching 500 records

url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
headers = {
    'accept': 'application/json',
    'access_token': 'fe66583bfe5185048c66571293e0d358'
}

 

pages = []

 

for offset in range(0, 500, 100):
    parameters = {
        'limit': 100,
        'offset': offset
    }

 

    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    pages.extend(data['data'])
main_dict = {'records': pages}


# In[304]:


len(main_dict['records'])


# In[116]:


headers


# In[180]:


df = data['data']
df[1]


# In[122]:


df = pd.DataFrame(data['data'][0])
df.T


# In[188]:


orders_by_customer = {}
for id in range(0, 2):

    # Optional: Create a dictionary of parameters for pagination
    url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales?offset='+str(id)+'&limit=30'
    headers = {
        'accept': 'application/json',
        'access_token': 'fe66583bfe5185048c66571293e0d358'
    }



    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        data = response.json()



        # Process and work with the data here



    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        
    df = data['data']
    for vals in df:
        customer_id = vals['order']['customer']['customer_id']
        if customer_id in orders_by_customer:
            orders_by_customer[customer_id] += 1
        else:
            orders_by_customer[customer_id] = 1
    
for customer_id, order_count in orders_by_customer.items():
    print(f"Customer ID: {customer_id}, Order Count: {order_count}")


# In[306]:


json_data = main_dict['records']
json_data


# In[307]:


df_json = pd.json_normalize(json_data)
df_json


# In[308]:


df_json.columns


# In[309]:


new_df = df_json[['id', 'sales_amt', 'qty', 'discount', 'profit_amt',
                  'order.order_id','order.order_purchase_date','order.order_status',
                  'order.order_delivered_customer_date','order.order_estimated_delivery_date',
                  'product.product_id','product.colors','product.category','order.customer.customer_id',
                  'order.customer.customer_name','order.vendor.VendorID']]


# In[310]:


new_df.head()


# In[311]:


new_df = df_json[['id', 'sales_amt', 'qty', 'discount', 'profit_amt',
                  'order.order_id','order.order_purchase_date','order.order_status',
                  'order.order_delivered_customer_date','order.order_estimated_delivery_date',
                  'product.product_id','product.colors','product.category','order.customer.customer_id',
                  'order.customer.customer_name','order.vendor.VendorID']]
new_df.rename(columns = {'order.order_id':'order_id', 'order.order_purchase_date':'order_purchase_date',
                              'order.order_status':'order_status','order.order_delivered_customer_date':'order_delivered_customer_date',
                         'order.order_estimated_delivery_date':'order_estimated_delivery_date','product.product_id':'product_id','product.colors':'colors',
                        'product.category':'category','order.customer.customer_id':'customer_id','order.customer.customer_name':'customer_name','order.vendor.VendorID':'VendorID'}, inplace = True)


# In[312]:


new_df


# In[322]:


new_df.replace('null',None, inplace = True)


# In[323]:


new_df.isnull().sum()


# In[316]:


new_df.info()


# In[317]:


duplicate = new_df[new_df.duplicated()]
duplicate


# In[318]:


new_df['order_purchase_date'] = pd.to_datetime(new_df['order_purchase_date'])


# In[319]:


new_df['day_of_order'] = new_df['order_purchase_date'].dt.weekday


# In[320]:


new_df.head()


# In[321]:


day_labels = {0: 'Weekday', 1: 'Weekday', 2: 'Weekday', 3: 'Weekday', 4: 'Weekday', 5: 'Weekend', 6: 'Weekend'}

new_df['day_label'] = new_df['day_of_order'].map(day_labels)


# In[325]:


new_df.head()


# In[324]:


len(new_df[new_df['day_label']=='Weekend'])


# In[326]:


higest_in_weekday =  new_df.loc[new_df['day_label'] == 'Weekday', 'sales_amt'].sum()
higest_in_weekend =  new_df.loc[new_df['day_label'] == 'Weekend', 'sales_amt'].sum()


# In[327]:


print("weekday:", higest_in_weekday)
print("weekend:", higest_in_weekend)


# In[329]:


cat_df = df_json[['sales_amt','product.category']]


# In[333]:


sales_by_category = cat_df.groupby('product.category')['sales_amt'].sum()
sales_by_category.reset_index()


# In[ ]:




