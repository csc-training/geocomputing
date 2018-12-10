# PostGIS management

## Basic commands in PostGRES PostGIS

Login to psql without password:
- `sudo -u postgres psql db_name`

Create a user:
- `CREATE ROLE user_name LOGIN PASSWORD 'your_password' SUPERUSER;``

Set/reset password to an existing user:
- `ALTER USER user_name WITH PASSWORD 'new_password';`
- ... or manually: `\password user_name`

## Other PostGIS general management commands
Review the tables size in disk
````
SELECT
   relname AS "Table",
   pg_size_pretty(pg_total_relation_size(relid)) As "Size",
   pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) as "External Size"
   FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;
````

Select random rows to show:
See the fields of pg_catalog.pg_statio_user_tables
````
   \d pg_catalog.pg_statio_user_tables
````

````
	SELECT *
	FROM flickr_data_hma
	order by random()
	limit 100;
````
Review important db settings
````
SELECT name, context, unit, setting, boot_val, reset_val
FROM pg_settings
WHERE name IN ( 'listen_addresses', 'max_connections', 'shared_buffers', 'effective_cache_size', 'work_mem', 'maintenance_work_mem');
````
## Spatial data management
**Checking and fixing geometry_columns**

In case you need to fix geometry details for SRID code, you can check the spatial column with:
```
SELECT f_table_name, f_geometry_column, srid, type
	FROM geometry_columns
	WHERE f_table_name = 'your_table';


  f_table_name   | f_geometry_column | srid |   type
-----------------+-------------------+------+----------
 your_table | geom              |    0 | GEOMETRY

```

Note that the SRID code is not specified above.

To fix that, to for example SRID 4326:
```
SELECT populate_geometry_columns('public.your_table'::regclass);

SELECT f_table_name, f_geometry_column, srid, type
	FROM geometry_columns
	WHERE f_table_name = 'your_table';


  f_table_name   | f_geometry_column | srid | type
-----------------+-------------------+------+-------
 your_table | geom              | 4326 | POINT
 ```
Now srid and type are correct after fixing geometry columns

See more info from the PostGIS documentation about [registering spatial colums](https://postgis.net/docs/using_postgis_dbmanagement.html#Manual_Register_Spatial_Column).

**Reprojecting table data in order to enable spatial query**

You can reproject your table data with:
```
ALTER TABLE your_table
 ALTER COLUMN geom TYPE geometry(Point,3879)
  USING ST_Transform(geom,3879);
```

**Adding other GIS data to POSTGIS**

You can import more data to your PostGIS from the command line with:
```
shp2pgsql -s 3879 new_data.shp public.new_data | psql -U student_user -h localhost -d postgres
```

## Connect to PostGIS database from GeoServer
If you want to make use of the PostGIS database from GeoServer, see the steps from the [PostGIS GeoServer documentation](https://docs.geoserver.org/stable/en/user/data/database/postgis.html).

Note that, to be able to login in to PostGIS via localhost from GeoServer you need to configure you PostGIS database configuration file (pg_hba.conf) to include configuration for `host` allowing local connections.
