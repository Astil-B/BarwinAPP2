CREATE TYPE user_role      AS ENUM ('manager', 'volunteer');
CREATE TYPE signup_status  AS ENUM ('confirmed', 'waitlisted');
CREATE TYPE drink_category AS ENUM ('beer', 'wine', 'cocktail', 'soft', 'other');

CREATE TABLE app_user (
    id          BIGSERIAL    PRIMARY KEY,
    username    VARCHAR(50)  UNIQUE NOT NULL,
    full_name   VARCHAR(100) NOT NULL,
    password    VARCHAR(120) NOT NULL,          -- bcrypt hash
    role        user_role    NOT NULL DEFAULT 'volunteer'
);
CREATE INDEX ix_app_user_username ON app_user (username);


CREATE TABLE event (
    id          BIGSERIAL    PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    date        DATE         NOT NULL,
    description TEXT,
    location    VARCHAR(200)
);

CREATE TABLE volunteer (
    id          BIGSERIAL    PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(20)
);

CREATE TABLE shift (
    id          BIGSERIAL    PRIMARY KEY,
    event_id    BIGINT       NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    role        VARCHAR(100) NOT NULL,
    start_time  TIMESTAMPTZ  NOT NULL,
    end_time    TIMESTAMPTZ  NOT NULL,
    capacity    INTEGER      NOT NULL DEFAULT 1
);
CREATE INDEX ix_shift_event_id ON shift (event_id);

CREATE TABLE shift_signup (
    id            BIGSERIAL     PRIMARY KEY,
    shift_id      BIGINT        NOT NULL REFERENCES shift(id)     ON DELETE CASCADE,
    volunteer_id  BIGINT        NOT NULL REFERENCES volunteer(id) ON DELETE CASCADE,
    status        signup_status NOT NULL DEFAULT 'confirmed',
    CONSTRAINT uq_signup UNIQUE (shift_id, volunteer_id)
);
CREATE INDEX ix_signup_shift_id     ON shift_signup (shift_id);
CREATE INDEX ix_signup_volunteer_id ON shift_signup (volunteer_id);

CREATE TABLE drink (
    id          BIGSERIAL      PRIMARY KEY,
    name        VARCHAR(100)   NOT NULL,
    category    drink_category,
    price_dkk   NUMERIC(6, 2)  NOT NULL,
    unit        VARCHAR(20)
);

CREATE TABLE sale (
    id            BIGSERIAL   PRIMARY KEY,
    event_id      BIGINT      NOT NULL REFERENCES event(id)     ON DELETE CASCADE,
    drink_id      BIGINT      NOT NULL REFERENCES drink(id),
    volunteer_id  BIGINT      NOT NULL REFERENCES volunteer(id),
    quantity      INTEGER     NOT NULL DEFAULT 1,
    sold_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_sale_event_id     ON sale (event_id);
CREATE INDEX ix_sale_drink_id     ON sale (drink_id);
CREATE INDEX ix_sale_volunteer_id ON sale (volunteer_id);
