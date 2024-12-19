--SELECT people.id FROM people WHERE people.name = 'Bradley Cooper'
--SELECT people.id FROM people WHERE people.name = 'Jennifer Lawence'

--SELECT stars.movie_id FROM stars WHERE stars.person_id = (people.id)
--SELECT stars.movie_id FROM stars WHERE stars.person_id = (people.id)

--SELECT movies.name FROM movies WHERE movies.id IN (stars.movie_id) AND movies.id IN (stars.movie_id)

SELECT movies.title FROM movies WHERE movies.id IN (SELECT stars.movie_id FROM stars WHERE stars.person_id = (SELECT people.id FROM people WHERE people.name = 'Bradley Cooper')) AND movies.id IN (SELECT stars.movie_id FROM stars WHERE stars.person_id = (SELECT people.id FROM people WHERE people.name = 'Jennifer Lawrence'));
