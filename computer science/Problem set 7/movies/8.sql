--SELECT movies.id FROM movies WHERE movies.title = 'Toy Story'
--SELECT stars.person_id FROM stars WHERE stars.movie_id = (id)
--SELECT people.name FROM people WHERE people.id IN (person_id)
SELECT people.name FROM people WHERE people.id IN (SELECT stars.person_id FROM stars WHERE stars.movie_id = (SELECT movies.id FROM movies WHERE movies.title = 'Toy Story'));
