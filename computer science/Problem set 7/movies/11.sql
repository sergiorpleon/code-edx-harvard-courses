--SELECT people.id FROM people WHERE people.name = 'Chadwick Boseman'
--SELECT stars.movie_id FROM stars WHERE stars.person_id = (people.id)
--SELECT ratings.movie_id FROM ratings WHERE ratings.movie_id IN (stars.movie_id) ORDER BY ratings.rating DESC LIMIT 5
--SELECT movies.title FROM movies WHERE movies.id IN (ratings.movie_id)

--SELECT movies.title FROM movies WHERE movies.id IN (SELECT ratings.movie_id FROM ratings WHERE ratings.movie_id IN (SELECT stars.movie_id FROM stars WHERE stars.person_id = (SELECT people.id FROM people WHERE people.name = 'Chadwick Boseman')) ORDER BY ratings.rating DESC LIMIT 5);

SELECT movies.title FROM movies
JOIN ratings ON ratings.movie_id = movies.id
JOIN stars ON stars.movie_id = movies.id
JOIN people ON people.id = stars.person_id
WHERE people.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;
