# HLS STAC Geoparquet DPS Demo

Demonstrate how to query the HLS STAC Geoparquet archive in a DPS job

## Motivation

The CMR STAC API has imposed rate limits on the HLS collections. Users can query this archive of the HLS STAC records directly from parquet files in S3 without any API rate limits.

## About

This DPS algorithm uses [`rustac`](https://github.com/stac-utils/rustac-py) to query an archive of HLS STAC records stored as STAC Geoparquet. By using `rustac` + parquet files there is no API between the requester and the actual data!

Try this out if you want to query HLS STAC records in your DPS jobs.

> [!WARNING]
> This archive of HLS STAC records is experimental and only contains items through May 2025.
