#!/usr/bin/env bash
hashes=`find -name 'Pipeline_*.profraw' | cut -d_ -f2 | sort | uniq`

for h in $hashes; do
	llvm-profdata merge "Pipeline_$h"_*.profraw -output="Pipeline_$h".profdata $@
done
