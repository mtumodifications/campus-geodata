-- All rooms on ground floor
SELECT
    fid,
    room_number,
    room_description,
    floor_level,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 0;

-- All rooms on first floor
SELECT
    fid,
    room_number,
    room_description,
    floor_level,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 1;

-- Ground floor rooms in A Block
SELECT
    fid,
    room_number,
    room_description,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 0
    AND building_block = 'A';

-- First floor rooms in A Block
SELECT
    fid,
    room_number,
    room_description,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 1
    AND building_block = 'A';

-- Ground floor toilets
SELECT
    fid,
    room_number,
    room_description,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 0
    AND LOWER(room_description) LIKE '%toilet%';

-- First floor toilets
SELECT
    fid,
    room_number,
    room_description,
    building_block,
    geom
FROM
    main_building_rooms
WHERE
    floor_level = 1
    AND LOWER(room_description) LIKE '%toilet%';