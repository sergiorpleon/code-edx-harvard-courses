--SELECT movies.id FROM movies WHERE movies.year = '2004'
--SELECT stars.person_id FROM stars WHERE stars.movie_id IN (id)
--SELECT people.name FROM people WHERE people.id IN (person_id)

SELECT people.name FROM people WHERE people.id IN (SELECT stars.person_id FROM stars WHERE stars.movie_id IN (SELECT movies.id FROM movies WHERE movies.year = '2004')) ORDER BY people.birth;
