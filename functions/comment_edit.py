# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 09:54:06 2020

@author: bolim
"""

class functions(object):
## Function that returns first 250 comments from NYTimes article in pandas dataframe


    def url_generate(self, url_in):
        """generates urls suitable for making NYTimes comment API requests. Need NYTimes API"""
        import re
        import os

        nyt_key = os.getenv("NYT_API_KEY")

        base_url = 'https://api.nytimes.com/svc/community/v3/'
        offset = ['0', '25', '50', '75', '100', '125', '150', '175', '200']

    # url_list to store generated urls
        url_list = []

        # cleaning up just one more
        url_clean = re.split('.html', url_in)[0]+'.html'


    # for loop to generate the urls
        for a in range(0, len(offset)):
            comment_api = 'user-content/url.json?api-key=' + nyt_key + '&offset=' + offset[a] + '&url='
            article_url = url_clean
            article_tmp1 = re.sub(':', '%3A', article_url)
            article_tmp2 = re.sub('/', '%2F', article_tmp1)

            final_url = base_url + comment_api + article_tmp2

            url_list.append(final_url)

        return url_list



    def url_call(self, url_list_in):
        """loops through the generated urls that are suitable for making NYTimes comment API reuests.
        Returns JSON object. API call is limited to 30 requests per minute (personal bumped up)
        If you are using a usual API call, edit the time.sleep from 2 to 6"""
    #### GET request to API, store JSON objects
        import requests
        import time
    # json_list to store generated json objects
        json_list = []

    # make the first call and pass through if not able to make calls
        check_response = requests.get(url_list_in[0], params = {'sort':'oldest'})
        time.sleep(2) # first break for 2 seconds to not exceed API limit
        check_json_obj = check_response.json()

        if check_json_obj['results']['totalCommentsFound'] == 0:
            return(print("comments disabled in this article"))

        else:
    # for loop to generate the json objects
            for a in range(1, len(url_list_in)):
                response = requests.get(url_list_in[a], params = {'sort' : 'oldest'})
                # 2 second delay between API calls, not to exceed limit
                # :::::::: EDIT THIS TO 6 IF API CALL LIMIT IS 10 CALLS PER MINUTE:::::::::
                time.sleep(2)

                json_obj = response.json()
                json_list.append(json_obj)

            json_list.append(check_json_obj)

            return(json_list)



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
                result.append(re.sub(',','',str(i['userDisplayName'])) + ',' + re.sub(',','',str(i['userDisplayName'])).split(' ')[0] +',' + re.sub(',','',str(i['commentBody'])) + ','
                              + str(i['approveDate']) + ',' + str(i['recommendations']) + ',' + str(i['replyCount']) +','
                              + str(i['editorsSelection']))


        # save it in a pandas dataframe
        result_df = pd.DataFrame([cols.split(',') for cols in result],
                                  columns = ['userName', 'cleanName', 'comment', 'approveDate', 'n_recommend', 'n_reply', 'nyt_select']
                                  )

        result_df['ttlCommentNum'] = np.repeat(json_list_in[0]['results']['totalCommentsFound'], len(result_df))

        # transform data types
        result_df['n_recommend'] = result_df['n_recommend'].astype(int)
        result_df['n_reply'] = result_df['n_reply'].astype(int)
        result_df['approveDate'] = result_df['approveDate'].astype(int)
        result_df['comment'] = result_df['comment'].astype(str)

        # clean the name
        name_list = result_df['cleanName'].values.tolist()
        name_tmp = [name.lower() for name in name_list]
        name_tmp = [re.sub('[^a-z]', '', name) for name in name_tmp]
        result_df['cleanName'] = name_tmp

        # Add time
        result_df['time'] = np.repeat(None, len(result_df))

        for v in range(0, len(result_df)):
            result_df['time'].iloc[v] = datetime.fromtimestamp(result_df['approveDate'].iloc[v])

        # Add time_order index
        result_df = result_df.sort_values(by = 'time').reset_index(drop = True)
        result_df['time_order'] = np.arange(1, len(result_df)+1)
        result_df['time_order_cap'] = result_df['time_order'].clip(1,25)
        # Drop the approve date
        result_df = result_df.drop(['approveDate'], axis = 1)

        # Add url
        result_df['url'] = np.repeat(url_in, len(result_df))

        # Log some variables: 'n_recommend', 'ttlCommentNum'
        result_df['n_rec_log'] = np.log(np.asarray(result_df['n_recommend'])+1)
        result_df['ttl_comment_log'] = np.log(np.asarray(result_df['ttlCommentNum'])+1)

        # Add name gender classifier
        import pickle
        male_names = pickle.load(open('male_names.pkl', 'rb'))
        female_names = pickle.load(open('female_names.pkl', 'rb'))
        neutral_names = pickle.load(open('neutral_names.pkl','rb'))

        result_df['gender'] = np.repeat(None, len(result_df))

        for v in range(0, len(result_df)):
            # Clean the name structure
            if result_df['cleanName'].iloc[v] in neutral_names:
                result_df.loc[v, 'gender'] = 2
            elif result_df['cleanName'].iloc[v] in male_names:
                result_df.loc[v, 'gender'] = 0
            elif result_df['cleanName'].iloc[v] in female_names:
                result_df.loc[v, 'gender'] = 1
            else:
                result_df.loc[v, 'gender'] = 2


        # Add article date
        result_df['date'] = [re.findall('2020/[0-9][0-9]/[0-9][0-9]', text) for text in result_df['url']]
        result_df['date'] = result_df['date'].astype(str)

        # Add article category
        result_df['category'] = [re.findall('(?<=/2020/[0-9][0-9]/[0-9][0-9])/.*/.*/|(?<=/2020/[0-9][0-9]/[0-9][0-9])/.*/', text) for text in result_df['url']]
        result_df['category'] = result_df['category'].astype(str)

        result_df['date'] = [re.sub('\[|\]','',text) for text in result_df['date'].values.tolist()]
        cat_tmp = result_df['category'].values.tolist()
        cat_tmp2 = [re.sub('[\[\]]','',text) for text in cat_tmp]
        cat_tmp3 = [re.sub('^\/*|\/*$','',str(text)) for text in cat_tmp2]
        result_df['category'] = cat_tmp3
        
        # Add upper category (i.e. world/asia, world/europe -> world
        category_ = []
        for text in result_df['category']:
            try:
                tmp = re.split('/', text)[1]
                category_.append(tmp)
            except:
                category_.append("No category")

        result_df['category_'] = category_
        
        # Add business boolean
        result_df['biz'] = [bool(re.search('business', text)) for text in result_df['category_']]


        return result_df

    def loop_through(self, many_url_list):
        """loops through urls and returns a concatenated dataframe"""

        import pandas as pd
        import re

        # clean url format
        many_url_list_clean = [re.split('.html', url)[0]+'.html' for url in many_url_list]


        # final big dataframe
        big_df = pd.DataFrame()

        for url in many_url_list_clean:
            tmp_urls = self.url_generate(url)

            try:
                tmp_jsons = self.url_call(tmp_urls)
                if tmp_jsons == None:
                    big_df = big_df.append(pd.DataFrame())

                else:
                    df_append = pd.DataFrame()
                    tmp_df = self.parse_json(url, tmp_jsons)
                    df_append = df_append.append(tmp_df, ignore_index=True)
                    big_df = big_df.append(df_append, ignore_index = True)
            except:
                pass

        return(big_df)


    def get_all_articles_month(self, year, month):
        """gets all nyt articles of that year, month; requires NYT API"""

        import requests
        import os
        import re

        nyt_api_key = os.getenv("NYT_API_KEY")

        url = 'https://api.nytimes.com/svc/archive/v1/'+ year+'/'+month+'.json?api-key='+nyt_api_key
        response = requests.get(url)
        json_file = response.json()

        urls = []
        for i in json_file['response']['docs']:
            tmp = str(i['web_url'])
            # filter out sections without comments
            # obituaries, crosswords, weddings
            if bool(re.search('/obituaries|/crosswords|/fashion/weddings/', tmp)) == False:
                urls.append(tmp)

        # only get the unique urls
        urls = list(set(urls))

        # has to end with .html
        url_clean = []
        for i in urls:
            if i.endswith('.html') == True:
                url_clean.append(i)

        return(url_clean)
       