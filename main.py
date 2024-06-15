#importing required Libraries
import pandas as pd
from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from matplotlib import pyplot as plt

#Api Key
api_key = 'AIzaSyB4OXfpAAB77IWvcftsa8bGu8p5it5dATQ'

#Building Youtube Object
youtube = build('youtube',
                'v3',
                developerKey=api_key)

#Defining Function to Request Youtube API to Fetch Video Top Level Comments
def comment_downloader(youtube, id, pageToken=None, data=None):
    global df
    if data is None:
        data = {"Comments": [], "PublishedAt": [], "Author": [], "Like_Counts": [], "Reply_Comments": []}
        
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=id,
        maxResults=100,
        pageToken=pageToken)
    response = request.execute()
    
    for item in response['items']:
        data["Comments"].append(item['snippet']['topLevelComment']['snippet']['textOriginal'])
        data["PublishedAt"].append(item['snippet']['topLevelComment']['snippet']['publishedAt'])
        data["Author"].append(item['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        data["Like_Counts"].append(item['snippet']['topLevelComment']['snippet']['likeCount'])
        data["Reply_Comments"].append(item['snippet']['totalReplyCount'])

    nextpagetoken=response.get('nextPageToken')

    if nextpagetoken:
        comment_downloader(youtube, id, pageToken=nextpagetoken, data=data)
    else:
        df = pd.DataFrame(data=data)
        df.to_csv('comments.csv', header=True, index=False, encoding='utf-8')
    
    return df

#Reading Extracted Comments CSV File
def read_comments():
    global df
    df = pd.read_csv("comments.csv")

    #Initializing Sentiment Analyzer 
    analyzer = SentimentIntensityAnalyzer()

    #Mapping Sentiment Scores to dataframe
    for key, comment in enumerate(df["Comments"]):
        scores = analyzer.polarity_scores(comment)
        for keys in scores:
            df.loc[key,keys] = scores[keys]
    return df        

#Scatter Plot of Comments by Density
def Scatter_plot(df):
    plt.figure(figsize=(10,7))
    plt.scatter(x = [x for x in range(len(df['pos']))], y='pos', data=df, s=df['pos']*100, c="g")
    plt.scatter(x = [x for x in range(len(df['neg']))], y="neg", data=df, s=df['neg']*100, c="r")
    plt.xlabel("Comments")
    plt.ylabel("Density")
    plt.title('Sentiment Analysis Scores by Density')
    plt.legend()
    plt.savefig('Sentiment Analysis Scores by Density.png')
    plt.show()
    return df

#Bar Plot of Comments by Scores

def bar_plot(df):
    for key, x in enumerate(df['Comments']):
        for k in ['pos', 'neg']:
            if df.loc[key, k]>0.8 and k=='pos':
                df.at[key, "pos_range"] = "Extremely High"
            elif df.loc[key, k]>0.6 and k=='pos':
                df.at[key, "pos_range"] = "High"
            elif df.loc[key, k]>0.4 and k=='pos':
                df.at[key, "pos_range"] = "Above Average"
            elif df.loc[key, k]>0.2 and k=='pos':
                df.at[key, "pos_range"] = "Average"
            elif df.loc[key, k]>0.0 and k=='pos':
                df.at[key, "pos_range"] = "Little"
            elif df.loc[key, k]>0.8 and k=='neg':
                df.at[key, "neg_range"] = "Extremely High"
            elif df.loc[key, k]>0.6 and k=='neg':
                df.at[key, "neg_range"] = "High"
            elif df.loc[key, k]>0.4 and k=='neg':
                df.at[key, "neg_range"] = "Above Average"
            elif df.loc[key, k]>0.2 and k=='neg':
                df.at[key, "neg_range"] = "Average"
            elif df.loc[key, k]>0.0 and k=='neg':
                df.at[key, "neg_range"] = "Little"
            else:
                pass

    # Prepare data for bar plot
    pos_counts = df['pos_range'].value_counts()
    neg_counts = df['neg_range'].value_counts()

    plt.figure(figsize=(10, 7))

    pos_bar = plt.bar(x=pos_counts.index, height=pos_counts.values, data=df, width=0.5, label='Positive', align='center', color='#79E327')
    neg_bar = plt.bar(x=neg_counts.index, height=neg_counts.values, data=df, width=0.5, label='Negative', align='center', color='#F85D41')

    for bar in pos_bar:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y+1, y, ha='center', c="black")

    for bar in neg_bar:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y+1, y, ha='center', c='red')

    plt.xlabel("Comments", fontsize=14)
    plt.ylabel("Density", fontsize=14)

    plt.title('Sentiment Analysis Scores by Intensity')

    plt.legend()

    plt.savefig('Sentiment Analysis Scores by Range.jpeg')

    plt.show()

    df.to_csv("Output Comments.csv", header=True, index=False, encoding='utf-8')

#Requesting Youtube Video URL From User

#url =input("Enter Video URL: ")
#video_id = url.split('=')[1].split('&')[0]

#comment_downloader(youtube,video_id)
#df = read_comments()
#df = Scatter_plot(df)
#df = bar_plot(df)