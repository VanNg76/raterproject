SELECT *
FROM raterapi_game;

delete from raterapi_picture


insert into raterapi_game_categories
values (?, 3, 5);
insert into raterapi_game_categories
values (?, 1, 5);
insert into raterapi_game_categories
values (?, 1, 2);

drop table raterapi_picture;

insert into raterapi_review
values (?, "exciting game", 2, 1);

create table raterapi_picture (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`player_id`  INTEGER NOT NULL,
	`game_id` INTEGER NOT NULL,
	`link` TEXT NOT NULL
);
