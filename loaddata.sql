SELECT *
FROM raterapi_game;

delete from raterapi_picture


insert into raterapi_game_categories
values (?, 3, 5);
insert into raterapi_game_categories
values (?, 1, 5);
insert into raterapi_game_categories
values (?, 1, 2);

insert into raterapi_game_categories
values (?, 2, 4);
insert into raterapi_game_categories
values (?, 5, 4);
insert into raterapi_game_categories
values (?, 4, 2);

insert into raterapi_rate (rate, game_id, player_id)
values (8, 4, 2);
insert into raterapi_rate (rate, game_id, player_id)
values (7, 4, 1);
insert into raterapi_rate (rate, game_id, player_id)
values (6, 5, 2);

insert into raterapi_game (id, title, description, designer, year_released, number_of_players, estimate_time_to_play, age_recommendation, player_id)
values (4, "King Empire", "board battle", "K", 2010, 2, 30, 15, 1);

drop table raterapi_picture;

insert into raterapi_review
values (?, "exciting game", 2, 1);
insert into raterapi_review
values (?, "good game", 2, 1);
insert into raterapi_review
values (?, "very good game", 2, 1);

create table raterapi_picture (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`player_id`  INTEGER NOT NULL,
	`game_id` INTEGER NOT NULL,
	`link` TEXT NOT NULL
);


SELECT g.id, g.title, ra.rate, ra.game_id, ra.player_id,
		avg(ra.rate) as average_rate
FROM raterapi_game g
JOIN raterapi_rate ra
	ON ra.game_id = g.id
group by g.id

-- gamesbyrating
SELECT g.id, g.title, avg(ra.rate) AS average_rate
FROM raterapi_rate ra
JOIN raterapi_game g
	ON ra.game_id = g.id
GROUP BY g.id
ORDER BY average_rate

-- the most review game
SELECT GameId, GameTitle, MAX(number_of_reviews)
FROM (
SELECT g.id GameId, g.title GameTitle, COUNT(g.id) AS number_of_reviews
FROM raterapi_game g
JOIN raterapi_review re
	ON re.game_id = g.id
GROUP BY g.id
)

-- games by category
SELECT c.label Category, g.id GameId, g.title GameTitle
FROM raterapi_game g
JOIN raterapi_game_categories gc
	ON gc.game_id = g.id
JOIN raterapi_category c
	ON c.id = gc.category_id
