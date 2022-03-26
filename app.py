
import streamlit as st
import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

data = pd.read_csv('imdb_top_1000.csv')
feature_selection = ['Genre', 'Director', 'Star1', 'Star2', 'Star3', 'Star4', 'Overview']
data_selected = data[feature_selection]
data_selected['Genre'] = data_selected['Genre'].apply(lambda x: x.replace(',',''))
combine_feature = data_selected['Genre']+' '+data_selected['Director']+' '+data_selected['Star1']+' '+data_selected['Star2']+ ' '+data_selected['Star3']+' '+data_selected['Star4']+' '+data_selected['Overview']
list_all_titles = data['Series_Title'].tolist()
vectorizer = TfidfVectorizer()
feature_transform = vectorizer.fit_transform(combine_feature)
similarity = cosine_similarity(feature_transform)



def movie_recommend(movie_name = 'seven'):
  find_close_match = difflib.get_close_matches(movie_name, list_all_titles)    
  close_match = find_close_match[0]
  index_of_the_movie = data[data.Series_Title == close_match].index[0]         
  similarity_score = list(enumerate(similarity[index_of_the_movie]))           
  sorted_similar_movies_top5 = sorted(similarity_score, key = lambda x:x[1], reverse = True)[:6] 
  title_list = []
  poster_list = []
  for i in sorted_similar_movies_top5:                                        
    index = i[0]
    title = data[data.index==index]['Series_Title'].values[0]
    picture = data[data.index==index]['Poster_Link'].values[0]
    title_list.append(title)
    poster_list.append(picture)

  return title_list, poster_list

def get_recommend(movie_name):      # Define try,except function that contain movie_recommend function in case of error in user input
  try:
    title_list, poster_list = movie_recommend(movie_name = movie_name)
  except:
    random_name_list = np.random.choice(list_all_titles,5).tolist()
    print('\n')
    print('*'*20)
    print('Error is happen. Due to too much wrong spelling or out of list from IMDB1000. Try another Movie name.. \nMay be pick one from random list below vvv \n\n{}\n'.format(random_name_list))
    print('or from top 10 IMDBscore list below vvv \n\n{}\n'.format(list_all_titles[:10]))
    movie_recommend('Press for enter movie you like')
  finally:
    return title_list, poster_list


def run():

  st.title('**_Movie Recommendation Web Application_**')

  title = st.text_input('Write your intresed movie')

  if st.button('Show Recommendation'):
    try:
      title_list, poster_list = movie_recommend(movie_name = title)
    except:
      random_name_list = np.random.choice(list_all_titles,5).tolist()
      st.write('\n')
      st.write('*'*20)
      st.write('Error is happen. Due to too much wrong spelling or The movie is not ranked IMDB1000. Try another Movie name.. \nMay be pick one from random list below  \n\n{}\n'.format(random_name_list))
      st.write('or from top 10 IMDBscore list below  \n\n{}\n'.format(list_all_titles[:10]))

    st.write('Recommended Movie')

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
      st.image(poster_list[0],width=100,caption= 'Selected : {}'.format(title_list[0]))
    with col2:
      st.image(poster_list[1],width=100,caption=title_list[1])

    with col3:
      st.image(poster_list[2],width=100,caption=title_list[2])

    with col4:
      st.image(poster_list[3],width=100,caption=title_list[3])

    with col5:
      st.image(poster_list[4],width=100,caption=title_list[4])

    with col6:
      st.image(poster_list[5],width=100,caption=title_list[5])

if __name__ == '__main__':
	run()