#!/bin/bash

# Output file
echo "HashFunction TimeTaken" > signing_performance.dat

# Generate 100MB file
dd if=/dev/urandom of=100MB.file bs=1M count=100

# Hash functions to test
hash_functions=(sha3-256 sha3-512 ripemd160)

# Loop through the specified hash functions
for hash in "${hash_functions[@]}"; do
    total_time=0
    
    # Run signing 100 times
    for i in {1..100}; do
        time_taken=$( (time -p openssl dgst -$hash -sign private-secp256k1.pem -out 100MB.sig 100MB.file) 2>&1 | awk '/real/ {print $2}')
        total_time=$(echo "$total_time + $time_taken" | bc)
    done
    
    # Compute the average time for 100 runs
    avg_time=$(echo "scale=6; $total_time / 100" | bc)
 # Append results to the output file
    echo "$hash $avg_time" >> signing_performance.dat

done

echo "Signing performance measurement completed. Results saved in signing_performance.dat."
