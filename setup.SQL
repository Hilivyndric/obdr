CREATE TABLE points (
	id integer PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE users (
	id integer PRIMARY KEY AUTOINCREMENT,
	tg_id integer
);

CREATE TABLE images (
	id integer PRIMARY KEY AUTOINCREMENT,
	user_id integer,
	url string,
	comment text
);

CREATE TABLE pointsimages (
	id integer PRIMARY KEY AUTOINCREMENT,
	point_id integer,
	image_id integer
);