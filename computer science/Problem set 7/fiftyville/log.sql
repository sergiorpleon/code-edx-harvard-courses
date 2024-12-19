-- Keep a log of any SQL queries you execute as you solve the mystery.

--date: 28 Julio 2023
--street: Humphrey

SELECT description FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28 and street LIKE '%Humphrey%';
/*
Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
Littering took place at 16:36. No known witnesses.
*/

--Interviews
SELECT name, transcript FROM interviews WHERE transcript LIKE '%bakery%' AND year = 2023 AND month = 7 AND day = 28;
/*
Ruth|Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
Eugene|I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
Raymond|As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
*/

--Ruth|Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
--license_plate
SELECT license_plate FROM bakery_security_logs WHERE minute>=15 AND minute<=25 AND hour=10 AND activity='exit' AND year = 2023 AND month = 7 AND day = 28;
/* Cars leaving the parking lot between 10:15 and 10:25 that day
5P2BI95
94KL13X
6P58WS2
4328GD8
G412CB7
L93JTIZ
322W7JE
0NTHK55
*/
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE minute>=15 AND minute<=25 AND hour=10 AND activity='exit' AND year = 2023 AND month = 7 AND day = 28) ORDER BY name;
/* Car owners leaving the parking lot between 10:15 and 10:25 that day
243696|Barry|(301) 555-4174|7526138472|6P58WS2
686048|Bruce|(367) 555-5533|5773159633|94KL13X
514354|Diana|(770) 555-1861|3592750733|322W7JE
396669|Iman|(829) 555-5269|7049073643|L93JTIZ
560886|Kelsey|(499) 555-9472|8294398571|0NTHK55
467400|Luca|(389) 555-5198|8496433585|4328GD8
398010|Sofia|(130) 555-0289|1695452385|G412CB7
221103|Vanessa|(725) 555-4692|2963008352|5P2BI95
*/

--Eugene|I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
--I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
SELECT account_number  FROM atm_transactions WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street' AND year = 2023 AND month = 7 AND day = 28;
/* Account number from which money was withdrawn at the ATM of Leggett Street
28500762
28296815
76054385
49610011
16153065
25506511
81061156
26013199
*/
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number  FROM atm_transactions WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street' AND year = 2023 AND month = 7 AND day = 28)) ORDER BY name;
/* Account holders who withdrew money from the Leggett Street ATM on the day of the robbery
438727|Benista|(338) 555-6650|9586786673|8X428L0
458378|Brooke|(122) 555-4581|4408372428|QX4YZN3
686048|Bruce|(367) 555-5533|5773159633|94KL13X
514354|Diana|(770) 555-1861|3592750733|322W7JE
396669|Iman|(829) 555-5269|7049073643|L93JTIZ
395717|Kenny|(826) 555-1652|9878712108|30G67EN
467400|Luca|(389) 555-5198|8496433585|4328GD8
449774|Taylor|(286) 555-6063|1988161715|1106N58
*/

--Raymond|As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
SELECT caller FROM phone_calls  WHERE duration < 60 AND year = 2023 AND month = 7 AND day = 28;
/* Number that made calls lasting less than a minute on the day of the robbery
(130) 555-0289
(499) 555-9472
(367) 555-5533
(499) 555-9472
(286) 555-6063
(770) 555-1861
(031) 555-6622
(826) 555-1652
(338) 555-6650
*/
SELECT * FROM people WHERE phone_number IN (SELECT caller FROM phone_calls  WHERE duration < 60 AND year = 2023 AND month = 7 AND day = 28) ORDER BY name;
/* Phone owners who made calls lasting less than a minute on the day of the robbery
438727|Benista|(338) 555-6650|9586786673|8X428L0
686048|Bruce|(367) 555-5533|5773159633|94KL13X
907148|Carina|(031) 555-6622|9628244268|Q12B3Z3
514354|Diana|(770) 555-1861|3592750733|322W7JE
560886|Kelsey|(499) 555-9472|8294398571|0NTHK55
395717|Kenny|(826) 555-1652|9878712108|30G67EN
398010|Sofia|(130) 555-0289|1695452385|G412CB7
449774|Taylor|(286) 555-6063|1988161715|1106N58
*/

--Raymond|I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
SELECT id FROM flights WHERE origin_airport_id = (SELECT id from airports WHERE city='Fiftyville') AND year = 2023 AND month = 7 AND day = 29 ORDER BY hour, minute LIMIT 1;
/* First flight ID of the day after the robbery
36
*/

SELECT city FROM airports WHERE id = (SELECT destination_airport_id FROM flights WHERE id = 36);
/* Destination of the first flight
The thief escaped = New York City
*/

SELECT passport_number FROM passengers WHERE flight_id = 36;
/* Passports of people who boarded the first flight the day after the robbery
7214083635
1695452385
5773159633
1540955065
8294398571
1988161715
9878712108
8496433585
*/
SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36) ORDER BY name;
/* People who boarded the first flight the day after the robbery
686048|Bruce|(367) 555-5533|5773159633|94KL13X
953679|Doris|(066) 555-9701|7214083635|M51FA04
651714|Edward|(328) 555-1152|1540955065|130LD9Z
560886|Kelsey|(499) 555-9472|8294398571|0NTHK55
395717|Kenny|(826) 555-1652|9878712108|30G67EN
467400|Luca|(389) 555-5198|8496433585|4328GD8
398010|Sofia|(130) 555-0289|1695452385|G412CB7
449774|Taylor|(286) 555-6063|1988161715|1106N58
*/



SELECT name FROM people
WHERE id IN (SELECT id FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE minute>=15 AND minute<=25 AND hour=10 AND activity='exit' AND year = 2023 AND month = 7 AND day = 28))
AND id IN (SELECT id FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number  FROM atm_transactions WHERE transaction_type = 'withdraw' AND atm_location = 'Leggett Street' AND year = 2023 AND month = 7 AND day = 28)))
AND id IN (SELECT id FROM people WHERE phone_number IN (SELECT caller FROM phone_calls  WHERE duration < 60 AND year = 2023 AND month = 7 AND day = 28))
AND id IN (SELECT id FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36));
/* I intercept the parking, cashier, call and passenger lists
The thief  = Bruce
*/

SELECT name FROM people WHERE phone_number = (SELECT receiver FROM phone_calls  WHERE caller=(SELECT phone_number FROM people WHERE name = 'Bruce') AND duration < 60 AND year = 2023 AND month = 7 AND day = 28);
/*Find the owner who received the call from Bruce on the day of the robbery
The accomplice = Robin
*/
