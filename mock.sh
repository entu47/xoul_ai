#!/bin/bash

start_port=8000

# Number of mock instances
n=30

for (( i=0; i<n; i++ ))
do
    port=$((start_port + i))
    python mock.py --port $port &
done

wait
echo "All instances of mock have finished."
