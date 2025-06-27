# HLS STAC Geoparquet DPS Demo

Demonstrate how to query the HLS STAC Geoparquet archive in a DPS job

## Motivation

The CMR STAC API has imposed rate limits on the HLS collections. Users can query this archive of the HLS STAC records directly from parquet files in S3 without any API rate limits.

## About

This DPS algorithm uses [`rustac`](https://github.com/stac-utils/rustac-py) to query an archive of HLS STAC records stored as STAC Geoparquet. By using `rustac` + parquet files there is no API between the requester and the actual data!

Try this out if you want to query HLS STAC records in your DPS jobs.

> [!WARNING]
> This archive of HLS STAC records is experimental and only contains items through May 2025.

## Details

The partitioned parquet dataset is available in my shared folder in the `maap-ops-workspace` bucket. The MAAP ADE and DPS both will have permissions to read from the archive.

See below for an example of how to run a basic query against the STAC geoparquet archive:

```python
from rustac import DuckdbClient


client = DuckdbClient(use_hive_partitioning=True)

# configure duckdb to find S3 credentials
client.execute(
    """
    CREATE OR REPLACE SECRET secret (
         TYPE S3,
         PROVIDER CREDENTIAL_CHAIN
    );
    """
)

# use rustac/duckdb to search through the partitioned parquet dataset to find matching items
results = client.search(
    href="s3://maap-ops-workspace/shared/henrydevseed/hls-stac-geoparquet-v1/year=*/month=*/*.parquet",
    datetime="2025-05-01T00:00:00Z/2025-05-31T23:59:59Z",
    bbox=(-90, 45, -85, 50),
)

```

`results` is a list of STAC items in dictionary form!
