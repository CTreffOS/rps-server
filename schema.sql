drop table if exists player;
create table player (
	id integer primary key,
	win integer default 0,
	played integer default 0,
	current text default Null,
	error text default Null
);
