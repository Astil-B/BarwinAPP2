INSERT INTO event (name, date, location, description) VALUES
    ('Sommerfest i blok 4', DATE '2026-06-05', 'Barwin', 'Sidste fest for skoleåret'),
    ('Galla for bioinformatik',      DATE '2026-06-12', 'Barwin', 'Kæmpe gallafest for bioinformatik');

INSERT INTO volunteer (name, email, phone) VALUES
    ('Ben Dover',   'Bend@barwin.dk', '+4520111213'),
    ('Biggus Dickus',    'Biggus@barwin.dk',   '+4520222324'),
    ('Mike Hunt ', 'Mike@barwin.dk', '+4520333435'),
    ('Cook Po',     'Cook@barwin.dk', '+4520444546');

INSERT INTO drink (name, category, price_dkk, unit) VALUES
    ('Tuborg Pilsner', 'beer',     25.00, '0.5L'),
    ('House Red',      'wine',     35.00, 'glass'),
    ('Gin & Tonic',    'cocktail', 45.00, 'glass'),
    ('Cola',           'soft',     15.00, '0.33L');


INSERT INTO shift (event_id, role, start_time, end_time, capacity) VALUES
    (1, 'bartender', TIMESTAMPTZ '2026-06-05 20:00+02', TIMESTAMPTZ '2026-06-05 23:00+02', 2);


INSERT INTO shift_signup (shift_id, volunteer_id, status) VALUES
    (1, 1, 'confirmed'),
    (1, 2, 'confirmed'),
    (1, 3, 'waitlisted');


INSERT INTO sale (event_id, drink_id, volunteer_id, quantity) VALUES
    (1, 1, 1, 3),
    (1, 3, 2, 1),
    (1, 4, 1, 4);
