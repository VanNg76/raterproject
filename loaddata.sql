SELECT *
FROM raterapi_game;

delete from raterapi_game
where id > 2

insert into raterapi_game_categories
values (?, 3, 5);
insert into raterapi_game_categories
values (?, 1, 5);
insert into raterapi_game_categories
values (?, 1, 2);

drop table raterapi_game_categories

insert into raterapi_review
values (?, "exciting game", 2, 1);