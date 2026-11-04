CREATE OR REPLACE FUNCTION get_building_rooms(
    selected_floor INTEGER
)
RETURNS JSON
LANGUAGE SQL
STABLE
AS $$
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', COALESCE(
            json_agg(
                json_build_object(
                    'type', 'Feature',
                    'id', id,
                    'properties', json_build_object(
                        'fid', fid,
                        'room_number', room_number,
                        'room_description', room_description,
                        'floor_level', floor_level,
                        'building_block', building_block
                    ),
                    'geometry', ST_AsGeoJSON(geom)::json
                )
            ),
            '[]'::json
        )
    )
    FROM public.main_building_rooms
    WHERE floor_level = selected_floor;
$$;
