#!/bin/bash

time=15
connections=40

select=`/usr/local/pgsql/bin/pgbench -c $connections    -T $time  gj | grep tps | grep including | awk '{x=$3+0.5; y=int(x); print y; }'`
insert=`/usr/local/pgsql/bin/pgbench -c $connections -S -T $time  gj | grep tps | grep including | awk '{x=$3+0.5; y=int(x); print y; }'`

f=$(($(($select))+$(($insert))))

echo $(($f))

