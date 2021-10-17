#!/bin/sh
# Run with root privileges
port=${port:-1505}
keep_open=${keep_open:-1} # 1 = True, 0 = False

while [ $# -gt 0 ]; do

  if [[ $1 == *"--"* ]]; then
    param="${1/--/}"
    declare "$param"="$2"
    echo "$1" "$2"
  fi

  shift
done

if (($keep_open == 1)); then
    ncat -nlv -p $port -k
else 
    ncat -nlv -p $port
fi

# -l -- listening mode
# -n -- no DNS
# -v -- verbose
# -k -- continue after client disconnects

echo "I am listening on $port"
