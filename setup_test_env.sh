#!/bin/bash

export PGDATA=/tmp/pgbench

if [ -d $PGDATA ]
then
  /usr/local/pgsql/bin/pg_ctl -D $PGDATA -w -m immediate stop

  rm -rf $PGDATA
fi

mkdir $PGDATA


/usr/local/pgsql/bin/initdb -D $PGDATA
/usr/local/pgsql/bin/pg_ctl -D $PGDATA -l /tmp/pgctl.log -w start
/usr/local/pgsql/bin/createdb gj
/usr/local/pgsql/bin/pgbench -i -F 100 -s 3000 gj

