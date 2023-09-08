# import necessary pacakges
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from flask import Flask, render_template
from datetime import datetime
# from flask_fontawesome import FontAwesome

from flask import Blueprint, g, escape, session, redirect, render_template, request, jsonify, Response, flash
from app import DAO
from Controllers.UserManager import UserManager

reco_view = Blueprint('reco_routes', __name__, template_folder='/templates')
reco_manager = UserManager(DAO)

recoGames = []

#Combine the values of the important columns into a single string
def get_important_features(data):
    important_features =[]
    for i in range(0,data.shape[0]):
        important_features.append(data['steamspy_tags'][i]+' '+data['name'][i])

    return important_features

import os
def runEngine(gameName):
    global new_df
    #Store data
    csv_path = './GameLibrary-All/steamgames.csv'
    df = pd.read_csv(csv_path)
    df.drop(['average_playtime', 'median_playtime', 'owners'], axis=1)
    # Find the row based on the cell element
    row_index = df.index[df['name'] == gameName][0]
    row = df.iloc[row_index]

    #Store data
    csv_path = './GameLibrary-Educational/educational_videogames.csv'
    new_df = pd.read_csv(csv_path)
    print("ALL1", new_df)

    df = pd.concat([new_df, pd.DataFrame([row])], ignore_index=True)
    df = df[df['positive_ratings'] >= 0]

    df = df.reset_index(drop = True)

    #List of important columns for recomendation
    columns =['name', 'developer', 'steamspy_tags', 'genres', 'desc', 'platforms']

    #Check for missing values
    df[columns].isnull().values.any()


    #Create a column to hold the strings
    df['important_features']=get_important_features(df)
    df['Game_no'] = range(0,df.shape[0])

    #Convert to matrix
    cm = CountVectorizer().fit_transform(df['important_features'])

    #Get the cosine similarity matrix from cm
    cs = cosine_similarity(cm)

    #Get the title the user likes
    title = gameName

    #Find the appid
    app_id = df[df.name == title]['Game_no'].values[0]

    #Create a list of similarity score
    scores = list(enumerate(cs[app_id]))

    #Sort the list
    sorted_scores = sorted(scores,key = lambda x:x[1],reverse = True)
    sorted_scores = sorted_scores[1:]

    df['positive_ratings'] = df['positive_ratings'].astype(str)

    #Print the first 10 recomended game
    j = 0
    recommendedGames = []
    recommendedGamesSimilarity = []
    print ('10 recomended game for',title,'are:\n')
    for item in sorted_scores:
        cell = df.iloc[item[0]:item[0]+1]
        game_title = (df[df.Game_no == item[0]]['name'].values[0]+' (Postitive Ratings : ' + df[df.Game_no == item[0]]['positive_ratings'].values[0] + ')')
        print(j+1,game_title)
        recommendedGames.append(df[df.Game_no == item[0]]['name'].values[0])
        print('Similarity : ',end='')
        print(item[1])
        recommendedGamesSimilarity.append((df[df.Game_no == item[0]]['name'].values[0], item[1]))
        j = j+1
        if j>9 :
            break

    return recommendedGamesSimilarity

def listOfGames(games):
  averages = defaultdict(list)
  for key, value in games:
      averages[key].append(value)

  result = [(key, sum(values) / len(values)) for key, values in averages.items()]
#   print("Result", result, len(result))
  return result

def displayAllGames():
    csv_path = './GameLibrary-Educational/educational_videogames.csv'
    games_df = pd.read_csv(csv_path)

    listOfGames = games_df['name'].tolist() 
    return listOfGames

def recommendForAllGames(gameList):
    global recoGames
    for gameName in gameList:
        likeGames = runEngine(gameName)
        recoGames.extend(likeGames)
    recommendedForAllGames = listOfGames(recoGames)
    sorted_data = sorted(recommendedForAllGames, key=lambda x: x[1], reverse=True)
    top = sorted_data[:]
    top = [item[0] for item in top]
    return top

def returnGameLink(gameNames):
    gameLinks = []
    for game in gameNames:
        gameLink = new_df.index[new_df['name'] == game][0]
        link = new_df.iloc[gameLink][14]
        gameLinks.append(link)
    return gameLinks

def returnGameImageLink(gameNames):
    gameImageLinks = []
    for game in gameNames:
        gameLink = new_df.index[new_df['name'] == game][0]
        link = new_df.iloc[gameLink][15]
        gameImageLinks.append(link)
    return gameImageLinks

def returnGameAgeReq(gameNames):
    gameAgeReq = []
    for game in gameNames:
        gameAge = new_df.index[new_df['name'] == game][0]
        age = new_df.iloc[gameAge][7]
        gameAgeReq.append(age)
    return gameAgeReq

def returnGameTags(gameNames):
    gameTags = []
    for game in gameNames:
        steam_tags = new_df.index[new_df['name'] == game][0]
        tags = new_df.iloc[steam_tags][10]
        tag_list = tags.split(";")
        selected_tags = tag_list[:3]
        selected_tags = ", ".join(selected_tags)
        gameTags.append(selected_tags)
    return gameTags

def create_5_star_rating(gameNames):
    gameRatings = []
    positiveRating = []
    for game in gameNames:
        gameLoc = new_df.index[new_df['name'] == game][0]
        negative_ratings = new_df.iloc[gameLoc][12]
        positive_ratings = new_df.iloc[gameLoc][11]

        if negative_ratings==0 and positive_ratings==0:
            rating, positive_ratings = 0, positive_ratings
        else:
            total_ratings = negative_ratings + positive_ratings
            percent_positive = positive_ratings / total_ratings
            star_rating = round(percent_positive * 5)
            rating, positive_ratings = star_rating, positive_ratings
        gameRatings.append(rating)
        positiveRating.append(positive_ratings)
    return gameRatings, positiveRating

def extractAge(birthdate):
    # Specify the given string
    # given_string = b
    # Convert the string to a datetime object
    given_date = datetime.strptime(str(birthdate), "%Y-%m-%d %H:%M:%S")

    # Get the current date
    current_date = datetime.utcnow()
    # Calculate the age
    age = current_date.year - given_date.year

    # Check if the birthday has already passed this year
    if current_date.month < given_date.month or (current_date.month == given_date.month and current_date.day < given_date.day):
        age -= 1

    return age

@reco_view.route('/main/', methods=['GET', 'POST'])
@reco_manager.user.login_required
def show_reco(id=None):
    reco_manager.user.set_session(session, g)
    userAge = extractAge(session['birthdate'])
    print("AGE",userAge)

    if id is None:
        id = int(reco_manager.user.uid())

    d = reco_manager.get(id)
    mygames = reco_manager.getGamesList(id)
    userGameList = []
    
    for game in mygames:
        userGameList.append(game['name'])

    options = ['5 stars', '4 stars', '3 stars', '2 stars', '1 star', 'No star']
    infoMessage = "No recommended games for you, please add games to your profile."
    if len(userGameList)!= 0:
        infoMessage = ""
        recommendToUser = recommendForAllGames(userGameList)
        
        gameAgeReq = returnGameAgeReq(recommendToUser)
        suggested_games = []
        for game, requirement in zip(recommendToUser, gameAgeReq):
            if requirement <= userAge:
                suggested_games.append(game)

        recommendToUser = suggested_games
        gameLinks = returnGameLink(recommendToUser)
        gameTags = returnGameTags(recommendToUser)
        gameRatings, positiveRating = create_5_star_rating(recommendToUser)
        imgLink = returnGameImageLink(recommendToUser)

        allGames = displayAllGames()
        allGames_gameLinks = returnGameLink(allGames)
        allGames_gameTags = returnGameTags(allGames)
        allGames_gameRatings, allGames_positiveRating = create_5_star_rating(allGames)
        allGames_imgLink = returnGameImageLink(allGames)
        # print("RATINGSALL",allGames_gameRatings)
        # print("recommendToUser", recommendToUser)
        # print("gameLinks", gameLinks)
        # print("gameRatings", gameRatings)
        # print("positiveRating", positiveRating)
        # print("imgLink", imgLink)
        
        filteredBy = ""
        # Zip the five lists together
        if request.method == 'POST':
            selected_option = request.form.get('option')

            selected_option = int(selected_option[0])
            
            games_data = zip(gameRatings, positiveRating, recommendToUser, gameLinks, imgLink, gameTags)
            allGames_data = zip(allGames_gameRatings, allGames_positiveRating, allGames, allGames_gameLinks, allGames_imgLink, allGames_gameTags)
            
            if selected_option != 6:
                filteredBy = "Filtered by " + str(selected_option) + " star ratings."
                # Filter games with 5 game ratings
                filtered_games = filter(lambda x: x[0] == selected_option, games_data)
                allGames_filtered_games = filter(lambda x: x[0] == selected_option, allGames_data)
                # print("SELECTED", selected_option, type(selected_option))

                # Sort the filtered games based on positive ratings
                sorted_games = sorted(filtered_games, key=lambda x: x[1], reverse=True)
                allsorted_games = sorted(allGames_filtered_games, key=lambda x: x[1], reverse=True)

                gameRatings = [game[0] for game in sorted_games]
                positiveRating = [game[1] for game in sorted_games]
                recommendToUser = [game[2] for game in sorted_games]
                gameLinks = [game[3] for game in sorted_games]
                imgLink = [game[4] for game in sorted_games]
                gameTags = [game[5] for game in sorted_games]

                allGames_gameRatings = [game[0] for game in allsorted_games]
                allGames_positiveRating = [game[1] for game in allsorted_games]
                allGames = [game[2] for game in allsorted_games]
                allGames_gameLinks = [game[3] for game in allsorted_games]
                allGames_imgLink = [game[4] for game in allsorted_games]
                allGames_gameTags = [game[5] for game in allsorted_games]

        bestGames_data = zip(allGames_gameRatings, allGames_positiveRating, allGames, allGames_gameLinks, allGames_imgLink, allGames_gameTags)
        bestGames_filtered_games = filter(lambda x: x[0] == 5, bestGames_data)
        # print("SELECTED", selected_option, type(selected_option))

        # Sort the filtered games based on positive ratings
        sorted_bestgames = sorted(bestGames_filtered_games, key=lambda x: x[1], reverse=True)

        bestGames_gameRatings = [game[0] for game in sorted_bestgames][:40]
        bestGames_positiveRating = [game[1] for game in sorted_bestgames][:40]
        bestGames_recommendToUser = [game[2] for game in sorted_bestgames][:40]
        bestGames_gameLinks = [game[3] for game in sorted_bestgames][:40]
        bestGames_imgLink = [game[4] for game in sorted_bestgames][:40]
        bestGames_gameTags = [game[5] for game in sorted_bestgames][:40]
        
        return render_template('recommend.html', gameName=recommendToUser, gameTags=gameTags, gameLink=gameLinks, gameRatings=gameRatings, positiveRating=positiveRating, imgLink=imgLink, options=options,  filteredBy=filteredBy,
                            allGames=allGames, allGames_gameTags=allGames_gameTags, allGames_gameLinks=allGames_gameLinks, allGames_gameRatings=allGames_gameRatings, allGames_positiveRating=allGames_positiveRating, allGames_imgLink=allGames_imgLink, 
                            bestGames=bestGames_recommendToUser, bestGames_gameTags=bestGames_gameTags, bestGames_gameLinks=bestGames_gameLinks, bestGames_gameRatings=bestGames_gameRatings, bestGames_positiveRating=bestGames_positiveRating, bestGames_imgLink=bestGames_imgLink, infoMessage=infoMessage, user=d)
    return render_template('recommend.html', infoMessage=infoMessage)