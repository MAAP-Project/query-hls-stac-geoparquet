import argparse
import asyncio
import logging
from pathlib import Path

import geopandas as gpd
import rustac
from rustac import DuckdbClient
from shapely.geometry import mapping

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def run(temporal: str, tile_idx: int, output_file: str):
    # read gpkg to get tile
    logger.info("reading tile geopackage")
    tile_gdf = gpd.read_file(
        "s3://maap-ops-workspace/shared/nathanmthomas/boreal_tiles_v003.gpkg"
    )

    logger.info(f"getting geometry for tile {tile_idx}")
    tile_geom = tile_gdf[tile_gdf["tile_num"] == tile_idx].to_crs(4326).geometry.iloc[0]

    # query HLS records for tile
    logger.info("querying HLS archive")
    client = DuckdbClient(use_hive_partitioning=True)
    client.execute(
        """
        CREATE OR REPLACE SECRET secret (
             TYPE S3,
             PROVIDER CREDENTIAL_CHAIN
        );
        """
    )
    results = client.search(
        href="s3://maap-ops-workspace/shared/henrydevseed/hls-stac-geoparquet-v1/year=*/month=*/*.parquet",
        datetime=temporal,
        intersects=mapping(tile_geom),
    )

    await rustac.write(href=output_file, value=results)


if __name__ == "__main__":
    parse = argparse.ArgumentParser(
        description="Queries the HLS STAC geoparquet archive and writes the result to a file"
    )
    parse.add_argument("--temporal", help="temporal range for the query", required=True)
    parse.add_argument("--tile_idx", help="boreal tile index", required=True, type=int)
    parse.add_argument(
        "--output_dir", help="Directory in which to save output", required=True
    )
    args = parse.parse_args()

    output_dir = Path(args.output_dir)
    output_file = str(output_dir / "hls.parquet")
    logging.info(
        f"running with temporal: {args.temporal}, output_file: {output_file}, tile_idx: {args.tile_idx}"
    )
    asyncio.run(
        run(temporal=args.temporal, output_file=output_file, tile_idx=args.tile_idx)
    )
