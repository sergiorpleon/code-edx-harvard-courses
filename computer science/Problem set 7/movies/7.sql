SELECT movies.title, ratings.rating FROM ratings JOIN movies ON movies.id = ratings.movie_id WHERE movies.year = 2010 AND ratings.rating not NULL ORDER BY ratings.rating DESC, movies.title;
