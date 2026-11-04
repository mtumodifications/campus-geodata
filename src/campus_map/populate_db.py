import geopandas as gpd

from pathlib import Path
from sqlalchemy import create_engine
from shapely.geometry import MultiPolygon

from config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

ROOM_FILES = [
    "data/geojson/rooms/cork_main_building_floor_0.geojson",
    "data/geojson/rooms/cork_main_building_floor_1.geojson",
]


def seed_rooms(file_path):

    print(f"\nImporting: {file_path}")

    gdf = gpd.read_file(file_path)

    if gdf.empty:
        print("No rooms found. Skipping.")
        return

    if gdf.crs is None:
        raise ValueError(f"Missing CRS in {file_path}")

    gdf = gdf.to_crs("EPSG:4326")

    # Rename columns
    gdf = gdf.rename(columns={
        "Room_Number": "room_number",
        "Room_Description": "room_description",
        "Level": "floor_level",
        "Block": "building_block"
    })

    # Validate columns
    required_columns = [
        "fid",
        "room_number",
        "room_description",
        "floor_level",
        "building_block",
        "geometry"
    ]

    missing = set(required_columns) - set(gdf.columns)

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    # Convert Polygon to MultiPolygon
    def convert_geometry(geom):
        if geom is None or geom.is_empty:
            return geom

        if geom.geom_type == "Polygon":
            return MultiPolygon([geom])

        if geom.geom_type == "MultiPolygon":
            return geom

        raise ValueError(
            f"Unexpected geometry type: {geom.geom_type}"
        )

    gdf["geometry"] = gdf["geometry"].apply(convert_geometry)

    # Rename geometry column
    gdf = gdf.rename_geometry("geom")

    # Select only database columns
    gdf = gdf[
        [
            "fid",
            "room_number",
            "room_description",
            "floor_level",
            "building_block",
            "geom"
        ]
    ]

    # Import into database
    gdf.to_postgis(
        name="main_building_rooms",
        con=engine,
        schema="public",
        if_exists="append",
        index=False
    )

    print(f"Successfully imported {len(gdf)} rooms.")


if __name__ == "__main__":

    try:
        for file_path in ROOM_FILES:

            if not Path(file_path).exists():
                print(f"File not found: {file_path}")
                continue

            seed_rooms(file_path)

        print("\nSupabase room import completed!")

    finally:
        engine.dispose()
