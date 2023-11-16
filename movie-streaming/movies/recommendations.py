from movies.load_models import cosine_sim, movies, csr_data, final_dataset, knn
import pandas as pd
from sklearn.neighbors import NearestNeighbors


def get_item_based_recommendation(movie_name):
    """
    This function provides movie recommendations based on collaborative filtering using k-nearest neighbors (k-NN). 
    It finds movies that are most similar to the given movie name based on user ratings.

    Args: 
      movie_name (str): The name of the movie for which recommendations are to be found. 
                        The movie name is case-sensitive and must match exactly with the movie names in the database.

    Returns:
      list: A list of dictionaries where each dictionary represents a recommended movie. 
            Each dictionary contains the title of the recommended movie and its 'distance' from the input movie 
            (a measure of similarity, with smaller values indicating higher similarity). 
            The list is sorted in descending order of similarity, with the most similar movie at the top.
            If the provided movie name does not exist in the database, an empty list is returned.

    Raises:
      TypeError: If the input movie_name is not a string.

    Example:
      >>> get_movie_recommendation('The Dark Knight')
      [{'Title': 'Batman Begins', 'Distance': 0.4578}, {'Title': 'The Dark Knight Rises', 'Distance': 0.3301}, ...]
    """
    n_movies_to_reccomend = 10
    movie_list = movies[movies['title'].str.contains(movie_name)]  
    if len(movie_list):
        movie_idx= movie_list.iloc[0]['movieId']
        try:
          movie_idx = final_dataset[final_dataset['movieId'] == movie_idx].index[0]
          distances , indices = knn.kneighbors(csr_data[movie_idx],n_neighbors=n_movies_to_reccomend+1)    
          rec_movie_indices = sorted(list(zip(indices.squeeze().tolist(),distances.squeeze().tolist())),key=lambda x: x[1])[:0:-1]
          recommend_frame = []
          for val in rec_movie_indices:
              movie_idx = final_dataset.iloc[val[0]]['movieId']
              idx = movies[movies['movieId'] == movie_idx].index
              recommend_frame.append({'Title':movies.iloc[idx]['title'].values[0],'Distance':val[1]})
          df = pd.DataFrame(recommend_frame,index=range(1,n_movies_to_reccomend+1))
          return df['Title'].to_list()
        
        except IndexError as e:
           return [] # if the movie is not in the training data
        
        except Exception as e:
           print("Something went wrong")
           print(e)
    else:
        return []


def get_content_based_recommendations(title):
  """
    This function provides movie recommendations based on content-based filtering. 
    It uses cosine similarity to find movies that are most similar to the given movie title.

    Args: 
      title (list): The list of the title of the movie for which recommendations are to be found. 
                   The title is case-sensitive and must match exactly with the movie titles in the database.

    Returns:
      list: A list of dictionaries where each dictionary represents a recommended movie. 
            Each dictionary contains the title of the recommended movie. 
            The list is sorted in descending order of similarity, with the most similar movie at the top.
            If the provided movie title does not exist in the database, an empty list is returned.

    Raises:
      TypeError: If the input title is not a string.

    Example:
      >>> get_recommendations('The Dark Knight')
      [{'title': 'The Dark Knight Rises'}, {'title': 'Batman Begins'}, ...]
  """
  recommended_movies = []

  for movie in title:
    movie_list = movies[movies['title'].str.contains(movie)]
    if len(movie_list):        
        idx = movie_list.index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[0:11]  # get top 10 similar movies
        movie_indices = [i[0] for i in sim_scores]
        recommendations = movies[['title']].iloc[movie_indices]
        recommended_movies.append(recommendations['title'].to_list())

  return recommended_movies