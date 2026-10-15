-- Schema for the time-booking system.
-- Run with: docker exec -i nhl-postgres psql -U nuser -d time_booking < schema.sql

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS rinks;
DROP TABLE IF EXISTS locker_rooms;

CREATE TABLE customers (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL CHECK (char_length(name) >= 5)
);

CREATE TABLE rinks (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (char_length(name) >= 5)
);

CREATE TABLE locker_rooms (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (char_length(name) >= 5)
);

CREATE TABLE bookings (
    id             INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_id    INTEGER NOT NULL REFERENCES customers(id),
    rink_id        INTEGER NOT NULL REFERENCES rinks(id),
    locker_room_id INTEGER NOT NULL REFERENCES locker_rooms(id),
    start_time     TIMESTAMP NOT NULL,
    duration       INTEGER NOT NULL CHECK (duration IN (60, 90, 120, 240))
);

CREATE INDEX idx_bookings_rink_start ON bookings(rink_id, start_time);
CREATE INDEX idx_bookings_locker_start ON bookings(locker_room_id, start_time);
CREATE INDEX idx_bookings_customer ON bookings(customer_id);