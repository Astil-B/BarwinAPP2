INSERT INTO event (name, date, location, description) VALUES
    ('Friday Bar — Semester Kickoff', DATE '2026-06-05', 'Barwin', 'First bar of the summer term.'),
    ('Friday Bar — Exam Relief',      DATE '2026-06-12', 'Barwin', 'Post-exam celebration night.');

INSERT INTO volunteer (name, email, phone) VALUES
    ('Alice Jensen',   'alice@barwin.dk', '+4520111213'),
    ('Bob Nielsen',    'bob@barwin.dk',   '+4520222324'),
    ('Clara Sørensen', 'clara@barwin.dk', '+4520333435'),
    ('David Holm',     'david@barwin.dk', '+4520444546');

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
