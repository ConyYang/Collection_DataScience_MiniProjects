import os
import pandas as pd
import pickle

data_folder = "ml-100k"
movie_name_filename = os.path.join(data_folder, "u.item")
movie_name_data = pd.read_csv(movie_name_filename,
                              delimiter="|",
                              header=None, encoding="mac-roman")

movie_name_data.columns = ["MovieID", "Title", "Release Date", "Video Release", "IMDB", "<UNK>", "Action", "Adventure", "Animation", "Children' s", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film- Noir", "Horror", "Musical", "Mystery", "Romance", "Sci- Fi", "Thriller", "War", "Western"]
with open("movieName.pkl", 'wb') as handle:
    pickle.dump(movie_name_data, handle)

def get_movie_name(movie_id):
    title_object = movie_name_data[movie_name_data["MovieID"] == movie_id]["Title"]
    title = title_object.values[0]
    return title
