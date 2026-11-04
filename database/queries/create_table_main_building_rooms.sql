CREATE TABLE IF NOT EXISTS
    main_building_rooms (
        id SERIAL PRIMARY KEY,
        fid INTEGER UNIQUE,
        room_number VARCHAR(20) UNIQUE,
        room_description VARCHAR(100),
        floor_level INTEGER,
        building_block VARCHAR(10),
        geom GEOMETRY (MULTIPOLYGON, 4326)
    );

CREATE INDEX IF NOT EXISTS main_building_rooms_geom_idx ON main_building_rooms USING GIST (geom);

ALTER TABLE main_building_rooms ENABLE ROW LEVEL SECURITY;