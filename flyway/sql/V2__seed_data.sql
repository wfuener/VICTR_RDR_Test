INSERT INTO events_tracking."user" (name, email) VALUES
    ('joe', 'joe@test_email.com'),
    ('emily', 'emily@test_email.com'),
    ('john', 'john@test_email.com'),
    ('ethan', 'ethan@test_email.com'),
    ('elaine', 'elaine@test_email.com')
;

INSERT INTO events_tracking."event" (user_id, title, description)
    select user_id, 'click', 'user clicked submit button' from events_tracking."user" ORDER BY random() limit 1;

INSERT INTO events_tracking."event" (user_id, title, description)
    select user_id, 'scroll up', 'scrolled up on details page' from events_tracking."user" ORDER BY random() limit 1;

INSERT INTO events_tracking."event" (user_id, title, description)
    select user_id, 'scroll down', 'scrolled down on home page' from events_tracking."user" ORDER BY random() limit 1;

INSERT INTO events_tracking."event" (user_id, title, description)
    select user_id, 'added item', 'laptop added to shopping cart' from events_tracking."user" ORDER BY random() limit 1;

INSERT INTO events_tracking."event" (user_id, title, description)
    select user_id, 'added item', 'keyboard added to shopping cart' from events_tracking."user" ORDER BY random() limit 1;



