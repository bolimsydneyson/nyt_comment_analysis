# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:54:06 2020

@author: bolim
"""

class functions(object):
## Function that returns first 250 comments from NYTimes article in pandas dataframe
    
    
    def url_generate(self, url_in):
        import re
        import os
        
        nyt_key = os.getenv("NYT_API_KEY")
        
        base_url = 'https://api.nytimes.com/svc/community/v3/'
        offset = ['0', '25', '50', '75', '100', '125', '150', '175', '200', '225']
    
    # url_list to store generated urls
        url_list = []
    
    # for loop to generate the urls
        for a in range(0, len(offset)):
            comment_api = 'user-content/url.json?api-key=' + nyt_key + '&offset=' + offset[a] + '&url='
            article_url = url_in
            article_tmp1 = re.sub(':', '%3A', article_url)
            article_tmp2 = re.sub('/', '%2F', article_tmp1)
        
            final_url = base_url + comment_api + article_tmp2
            
            url_list.append(final_url)
            
        return url_list
        


    def url_call(self, url_list_in):
    #### 2) GET request to API, store JSON objects
        import requests
        import time
    # json_list to store generated json objects    
        json_list = []
    
    # for loop to generate the json objects
        for a in range(len(url_list_in)):
            response = requests.get(url_list_in[a], params = {'sort' : 'oldest'})
            json_obj = response.json()
        
            json_list.append(json_obj)
            
        time.sleep(60) # delay for 60 seconds before making the next round of url calls

        return json_list



    def parse_json(self, url_in, json_list_in):
        """ Parses a list with many json objects from NYTimes comment API call. Returns a pandas dataframe"""
                      
        import pandas as pd
        import re
        import numpy as np
        from datetime import datetime
        
        # result list to store parsed json in csv format
        result = []
    
        # for loop to parse through json object
        for k in range(len(json_list_in)):
            for i in json_list_in[k]['results']['comments']:
                result.append(str(i['userDisplayName']) + ',' + str(i['userDisplayName']).split(' ')[0] +',' + re.sub(',',' ',str(i['commentBody'])) + ',' 
                              + str(i['approveDate']) + ',' + str(i['recommendations']) + ',' + str(i['replyCount']) +','
                              + str(i['editorsSelection']))  
                
    
        # save it in a pandas dataframe
        result_df = pd.DataFrame([cols.split(',') for cols in result],
                                  columns = ['userName', 'splitName', 'comment', 'approveDate', 'n_recommend', 'n_reply', 'nyt_select']
                                  )
        
        result_df['ttlCommentNum'] = np.repeat(json_list_in[0]['results']['totalCommentsFound'], len(result_df))
        
        # transform data types   
        result_df['n_recommend'] = result_df['n_recommend'].astype(int)
        result_df['n_reply'] = result_df['n_reply'].astype(int)
        result_df['approveDate'] = result_df['approveDate'].astype(int)
        result_df['comment'] = result_df['comment'].astype(str)
    
        # Add time
        result_df['time'] = np.repeat(None, len(result_df))

        for v in range(0, len(result_df)):
            result_df['time'].iloc[v] = datetime.fromtimestamp(result_df['approveDate'].iloc[v])
        
        # Add time_order index
        result_df = result_df.sort_values(by = 'time').reset_index(drop = True)
        result_df['time_order'] = np.arange(1, len(result_df)+1)
        # Drop the approve date
        result_df = result_df.drop(['approveDate'], axis = 1)
        
        # Add url
        result_df['url'] = np.repeat(url_in, len(result_df))        
        
        return result_df
        
    