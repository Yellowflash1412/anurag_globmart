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


# In[112]:


response1 = requests.get('https://globalmart-api.onrender.com/mentorskool/v1/sale')


# In[113]:


response1.status_code


# In[114]:


response1.headers['Content-Type']


# In[115]:


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


# In[190]:


data['data']


# In[ ]:





# In[ ]:





# In[ ]:




