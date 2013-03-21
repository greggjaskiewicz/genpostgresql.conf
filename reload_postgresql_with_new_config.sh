#!/bin/bash

# first param is the new configuration

export PGDATA=/tmp/pgbench

/usr/local/pgsql/bin/pg_ctl -D $PGDATA -l /tmp/pgctl.log -w stop

cp $1 $PGDATA/postgresql.conf

/usr/local/pgsql/bin/pg_ctl -D $PGDATA -l /tmp/pgctl.log -w start

