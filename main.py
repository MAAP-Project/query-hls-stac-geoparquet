import argparse
import asyncio
from pathlib import Path

import geopandas as gpd
import rustac
from shapely.geometry import mapping


async def run(temporal: str, tile_idx: int, output_file: str):
    # read gpkg to get tile
    print("reading tile geopackage")
    tile_gdf = gpd.read_file(
        "s3://maap-ops-workspace/shared/nathanmthomas/boreal_tiles_v003.gpkg"
    )

    print(f"getting geometry for tile {tile_idx}")
    tile_geom = tile_gdf[tile_gdf["tile_num"] == tile_idx].to_crs(4326).geometry.iloc[0]

    # query HLS records for tile
    print("querying HLS archive")
    await rustac.search_to(
        outfile=output_file,
        href="s3://maap-ops-workspace/shared/henrydevseed/hls-stac-geoparquet/v1/**/*.parquet",
        datetime=temporal,
        intersects=mapping(tile_geom),
    )


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        description="Queries the HLS STAC geoparquet archive and writes the result to a file"
    )
    parse.add_argument("--temporal", help="temporal range for the query", required=True)
    parse.add_argument("--tile_idx", help="boreal tile index", required=True)
    parse.add_argument(
        "--output_dir", help="Directory in which to save output", required=True
    )
    args = parse.parse_args()

    output_dir = Path(args.output_dir)
    output_file = str(output_dir / "hls.parquet")

    asyncio.run(
        run(temporal=args.temporal, output_file=output_file, tile_idx=args.tile_idx)
    )
