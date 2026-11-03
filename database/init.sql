CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE
    main_building_rooms (
        id SERIAL PRIMARY KEY,
        fid INTEGER UNIQUE,
        room_number VARCHAR(20) UNIQUE,
        room_description VARCHAR(100),
        floor_level INTEGER,
        building_block VARCHAR(10),
        geom GEOMETRY (MULTIPOLYGON, 4326)
    );

CREATE INDEX main_building_rooms_geom_idx ON main_building_rooms USING GIST (geom);