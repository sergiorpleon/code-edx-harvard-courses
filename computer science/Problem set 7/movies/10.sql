--SELECT ratings.id FROM ratings WHERE ratings.rating >= 9.0
--SELECT directors.person_id FROM directors WHERE directors.movie_id IN (id)
--SELECT people.name FROM people WHERE people.id IN (person_id)

SELECT people.name FROM people WHERE people.id IN (SELECT directors.person_id FROM directors WHERE directors.movie_id IN (SELECT ratings.movie_id FROM ratings WHERE ratings.rating >= 9.0));
