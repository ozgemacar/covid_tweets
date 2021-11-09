#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import matplotlib.pyplot as plt
import numpy as np


filepath = "ENTER YOUR FILEPATH HERE."
covid=pd.read_csv(filepath)
pd.options.display.max_colwidth = 500
covid = covid.drop(['id_str', 'user_id'],1) #This operation is held for hosting the code on Github.
covid


# Gives the number of lines and memory usage of the file in your system.  

print("There are", len(covid), "lines in the the dataframe.")
print()
print("The space that covid dataframe consumes in my memory for each column is as such:")
print(covid.memory_usage())
print()
print("In total, it consumes", covid.memory_usage(index=True).sum(), "bytes space in my memory.")


#Gives the column names of the file.

print("The column names are:")
for column_names in covid.columns:
    print(column_names)


#Identifies the most tweeting 50 users. 

print("The most tweeting 50 users are:")
most_tweeted_users=covid["screen_name"].value_counts().head(50)
print(most_tweeted_users)


#Plots the histogram of those the most tweeting 50 users.
covid_hist=covid[covid["screen_name"].str.contains('|'.join(most_tweeted_users.index))]
covid_hist

plt.hist(covid_hist["screen_name"], bins=50)
plt.title("Most Tweeting Users")
plt.xlabel("Users")
plt.ylabel("Number of tweets")


#Indentifies duplicated tweets.
print("Which tweets are duplicated?:")
print(covid.duplicated(subset=['text'], keep='first'))

duplicated_rows=covid[covid.duplicated(subset=['text'], keep='first')]
duplicated_rows


#Based on the text field, the code removes the duplicates while keeping the first. 
print("The number of tweets before removing duplicates is", len(covid))
covid_nonduplicated=covid.drop_duplicates(subset=['text'], keep='first')
print("The number of tweets after removing duplicates is", len(covid_nonduplicated))
covid_nonduplicated


#Replaces all users names in the 'text' field with the usrusr token.

covid_q7 = covid_nonduplicated.copy()
covid_q7['text']=covid_q7['text'].str.replace(r'@([a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*)', 'usrusr')
covid_q7


# Replaces all URLs with 'urlurl' token in the 'text' column.

covid_q8 = covid_q7.copy()
covid_q8['text']=covid_q8['text'].str.replace("https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,}", "urlurl")
covid_q8



# If a tweet starts with "RT @", it is a retweet. The code removes all retweets from the dataframe.

#I will continue with the dataframe from Question 8, so retweets will start with "RT usrusr"
covid_q9=covid_q8.copy()
covid_q9["RT or not"]=covid_q9['text'].str.contains("RT usrusr")
covid_q9=covid_q9.drop(covid_q9[covid_q9['RT or not'] == True].index)


#Then I will not need "RT or not" column anymore, so I can remove it.
covid_q9=covid_q9.drop(["RT or not"], axis=1)
covid_q9


# If the field is_retweet contains the value True, this tweet is a retweet as well. Remove those as well.

covid_q10 = covid_q9.copy()
covid_q10=covid_q10.drop(covid_q9[covid_q9['is_retweet'] == True].index)
covid_q10


# #### Question 11
# 
# Double check of the duplicate tweets and then the removal.
#covid_q11.duplicated(subset=["text"])
covid_q11=covid_q10.drop_duplicates(subset=['text'], keep='first')
print("The number of tweets that I have is", len(covid_q11))
covid_q11


#Plotting the histogram of the tweet lengths. 
#Deleting usrusr and urlurl from tweets in "text" column will help to count the length of the tweet itself.

covid_q12 = covid_q11.copy()
covid_q12["text"] = covid_q12["text"].str.replace("usrusr","")
covid_q12["text"] = covid_q12["text"].str.replace("urlurl","")
covid_q12["text_length"]=covid_q12.text.str.len()
print(covid_q12["text_length"])

plt.hist(covid_q12["text_length"], bins=20)
plt.title("Tweet Length vs. Number of tweets")
plt.xlabel("Length of the tweet")
plt.ylabel("Number of tweets")


#calculating the average tweet length.
average = covid_q12["text_length"].mean()
print("The average tweet length is", int(average))


# Extracting all words from the 'text' field and put them in a new column.
covid_q14 = covid_q12.copy()
covid_q14["words"]=covid_q14["text"].str.findall(r'(\w+)', flags=re.IGNORECASE)
covid_q14


# Identifyin the words that occur the most.

from collections import Counter

words_counter = Counter()
covid_q14['words'].apply(words_counter.update)
print(words_counter)


#Listing 100 of words that occur only once. Providing tweets that contain these words.


import operator
least_common100=words_counter.most_common()[:-101:-1]   
print("The length of the least_common100 list is", len(least_common100))
print()
print(least_common100)
print()
least_words=[]
for each_tuple in least_common100:
    least_words.append(each_tuple[0])

print("The length of the least_words list is", len(least_words))
print()
print(least_words)
print()
print("The sorted version of the least_words according to word length:")
sorted_least_words = sorted(least_words, key=len, reverse=True)
print(sorted_least_words)
print()
covid_q16=covid_q14[covid_q14["text"].str.contains(r'\b'+r'\b|\b'.join(sorted_least_words)+r'\b')]
covid_q16


# Finding the longest 100 words.

words=words_counter
word_length=[]
word_length = dict(words).keys()

sorted_length = sorted(word_length, key=len, reverse=True)

print("The number of words in the list is: %s." % (len(word_length)))
print("The shortest word in the list is: %s." % (sorted_length[-1]))
print("The longest word in the list is: %s." % (sorted_length[0]))
print()
print("The longest 100 words in the list are:")
sorted_length[0:100]


# Finding tweets that are all in upper case, such as "THIS IS A TWEET ALL UPPER CASE." in their 'text' field.

covid_q18=covid_q14[covid_q14['text'].str.isupper()]
print("There are", len(covid_q18), "tweets that are all in upper case.")
covid_q18


# Identifyng the mostly occurring 50 hashtags.

covid_q19 = covid_q14.copy()
covid_q19["hashtags"]=covid_q19["text"].str.findall(r"#(\w+)", flags=re.IGNORECASE)

hashtags={}

hashtag_counter = Counter()
covid_q19['hashtags'].apply(hashtag_counter.update)
hashtag_counter.most_common(50)



# Exporting the final dataframe to csv and Excel files.

#to Excel files:
covid_q19.to_excel(r'C:\Users\HP\Desktop\Özgem\Koç\Fall 2020\MAVA 354\Bonus Assignment - Özgem Elif Acar.xlsx', index = False, header=True)

#to csv files:
covid_q19.to_csv(r'C:\Users\HP\Desktop\Özgem\Koç\Fall 2020\MAVA 354\Bonus Assignment(csv) - Özgem Elif Acar.csv', index = False, header=True)

