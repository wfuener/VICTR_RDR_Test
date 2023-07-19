CREATE extension if not exists "uuid-ossp";

create schema events_tracking;

ALTER DATABASE events_db SET search_path TO public,events_tracking;

create table if not exists events_tracking."user"(
    user_id uuid default uuid_generate_v4() not null
		constraint user_pk
			primary key,
	name varchar(140),
	email varchar(140) not null,
	meta_create_ts timestamp default now()
);


create table if not exists events_tracking.event
(
	event_id uuid default uuid_generate_v4() not null
		constraint event_pkey
			primary key,
	user_id uuid not null
		constraint event_host_fkey
			references events_tracking."user",
	title varchar(140),
	description text,
	ts_title tsvector GENERATED ALWAYS AS (to_tsvector('english', title)) STORED,
	ts_description tsvector GENERATED ALWAYS AS (to_tsvector('english', description)) STORED,
    meta_create_ts timestamp default now(),
	meta_update_ts timestamp default now()
);

alter table events_tracking.event owner to api_admin;
-- Index on the foreign key (user_id)
create index event_user_fk_idx on events_tracking.event (user_id);


-- simple trigger to update timestamp on every update to a row
CREATE OR REPLACE FUNCTION meta_update_ts()
RETURNS TRIGGER AS $$
BEGIN
   NEW.meta_update_ts = now();
   RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER meta_update_ts AFTER UPDATE
ON events_tracking.event FOR EACH ROW EXECUTE PROCEDURE
meta_update_ts();

