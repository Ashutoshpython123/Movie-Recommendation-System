from flask import Flask, request, render_template, jsonify, Response, url_for
import json


import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def create_similarity():
    data = pd.read_csv('movie_data.csv')
    #create count matrix
    count_matrix = CountVectorizer().fit_transform(data['comb'])
    similarity = cosine_similarity(count_matrix)
    return data, similarity

def recommendation(movie):
    movie = movie.lower()
    data, similarity = create_similarity()
    
    if movie not in data['title'].unique():
        return('Sorry! this movie not present in database, please try other or check spelling.')
    else:
        index = data[data['title'] == movie].index[0]
        lst = list(enumerate(similarity[index]))
        sort_list = sorted(lst, key = lambda x:x[1], reverse=True)
        top_ten = sort_list[1:11] #except first
        
        rcmd = []
        for i in range(len(top_ten)):
            rcmd.append(data['title'][top_ten[i][0]])
        rcmd.append(movie)

        title = movie
        genres = data['genres'][index]
        actors = data['actors'][index]
        release_date = data['release_date'][index]
        imdb_rating = data['imdb_rating'][index]
        story = data['story'][index]

        rcmd_title = [title,genres,actors,release_date,imdb_rating,story]
    return rcmd, rcmd_title


app = Flask(__name__)


@app.route('/')
def home():
    data = pd.read_csv("movie_data.csv")
    suggestions  = list(data['title'].str.capitalize())
    return render_template('index.html', suggestions = suggestions)

#@app.route('/_autocomplete', methods=['GET'])
#def autocomplete():
 #   data = pd.read_csv("movie_data.csv")
  #  data_list = list(data['title'].str.capitalize())
   # return Response(json.dumps(data_list), mimetype='application/json')
 

@app.route('/recommended', methods=['GET','POST'])
def recommended():
    if request.method == 'POST':
            m = request.form['m']
    # poster path
    rcmd_poster = []
    data = pd.read_csv('movie_data.csv')
    rc_movie, rcmd_title = recommendation(m)
    for item in rc_movie:
        index = data[data['title'] == item].index[0]
        url = data['poster_path'][index]
        rcmd_poster.append(url)

    

    rcmd_movie =  rc_movie
    rcmd_url = rcmd_poster 
    
    suggestions  = list(data['title'].str.capitalize()) 

    return render_template('recomend.html',zip = zip, rcmd_movie=rcmd_movie, rcmd_url = rcmd_url, rcmd_title = rcmd_title, suggestions=suggestions)




if __name__ == "__main__":
    app.run(debug=True)
    
