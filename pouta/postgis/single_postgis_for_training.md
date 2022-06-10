# Single PostGIS VM for teaching
The aim of this guide is to set up PostGIS database for a university course with the following characteristics:
- The same PostGIS instance is used by several students.
- The teacher uses an existing table which is imported from a dump file after PostGIS has been installed.
- Students will use the database only to read data.

It is assumed that the installation has been done following the steps in [Basic PostGIS installation](basic_postgic.md).

## Basic set up

Export the PostGIS database you will use for the course to a dump file:
- `pg_dump -U postgres --table your_table --no-owner --no-reconnect --no-privileges -Fc some > /db/db-dumps/your_table.dump`

Import the course database to the course PostGIS database:
- `pg_restore -U student_user -h localhost -d postgres your_table.dump`

Create a user for the students to log in and give it read permissions to the schema where the table is located:
- `CREATE ROLE student_user LOGIN PASSWORD 'student_password';`
- `GRANT SELECT ON ALL TABLES IN SCHEMA public TO geostudent;`

## Student access to PostGIS
The virtual machine's security groups need to be set to allow access to port 5432 from the machines the students will be using. To improve security, it is recommended that you would open access to a limited IP range, for example to the IP range of the university's computer (for cPouta, see [Security Guidelines for cPouta](https://docs.csc.fi/cloud/pouta/security/)).

Set also the SSL mode to `SSL mode:prefer`


## Monitoring server's performance

In this section, some examples on how to review the PostGIS database performance.

### pgAdmin
Use pgAdmin Dashboard to see general information like ammount of connections and status.

Use also the SQL query tool to easily run commands on the database.


### Reviewing the logs
Depending on the settings in postgresql.conf the lenght of the log can be large. Check the last lines with
````
tail -100 /var/log/postgresql/postgresql-9.6-main.log
tail -f /var/log/postgresql/postgresql-9.6-main.log
ls -lah /var/log/postgresql/
````

### Managing the running processes
#### Review and kill processes from terminal
In case that the database is getting jammed, you can review the existing processes with pgAdmin in dashboard but also from the command line  and/or [stop processes](https://askubuntu.com/questions/547434/how-to-nicely-stop-all-postgres-processes) if needed.
````
ps -fHC postgres
ps -ef | grep postgres

kill <processid>
kill -9 <processid>
````

#### Review and kill processes with SQl
You can also manage processes from pgAdmin and/or [stop processes](https://medium.com/little-programming-joys/finding-and-killing-long-running-queries-on-postgres-7c4f0449e86d).

Show active connections
````
SELECT * FROM pg_stat_activity AS act
WHERE act.state='active';
````
Get a list of processes that have been running more than 5 minutes
````
SELECT * FROM pg_stat_activity
WHERE now()-state_change > '5 minute'::interval;
````

Get a list of processes that have been running less than 5 minutes, ordered by client's ip
````
SELECT * FROM pg_stat_activity
WHERE now()-state_change < '5 minute'::interval
order by client_addr;
````

Kill processes that have been idle for over 35 minutes
````
SELECT * FROM pg_stat_activity AS act
WHERE now()-state_change > '35 minute'::interval AND act.state='idle';
````
