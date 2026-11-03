GRANT USAGE ON SCHEMA public TO current_user;

GRANT
    USAGE,
    SELECT
ON ALL SEQUENCES IN SCHEMA public TO current_user;

GRANT
    SELECT,
    INSERT,
    UPDATE,
    DELETE
ON TABLE main_building_rooms TO current_user;

SELECT
    grantee,
    privilege_type
FROM
    information_schema.role_table_grants
WHERE
    table_name = 'main_building_rooms';