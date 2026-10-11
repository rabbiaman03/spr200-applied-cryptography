#!/bin/bash

# Output file
echo "Curve PrivReal PrivUser PrivSys PubReal PubUser PubSys" > ecc_keygen_perf.dat

# Loop through the specified curves
for curve in secp256k1 prime256v1 secp384r1 brainpoolP512t1; do
    priv_real=0 priv_user=0 priv_sys=0
    pub_real=0 pub_user=0 pub_sys=0
    
    # Run key generation 100 times
    for i in {1..100}; do
        priv_time=$( (time -p openssl ecparam -genkey -name "$curve" -noout -out private.pem) 2>&1 )
        pub_time=$( (time -p openssl ec -in private.pem -pubout -out public.pem) 2>&1 )
        
        priv_real=$(echo "$priv_real + $(echo "$priv_time" | awk '/real/ {print $2}')" | bc)
        priv_user=$(echo "$priv_user + $(echo "$priv_time" | awk '/user/ {print $2}')" | bc)
        priv_sys=$(echo "$priv_sys + $(echo "$priv_time" | awk '/sys/ {print $2}')" | bc)
        
        pub_real=$(echo "$pub_real + $(echo "$pub_time" | awk '/real/ {print $2}')" | bc)
        pub_user=$(echo "$pub_user + $(echo "$pub_time" | awk '/user/ {print $2}')" | bc)
        pub_sys=$(echo "$pub_sys + $(echo "$pub_time" | awk '/sys/ {print $2}')" | bc)
    done

 # Compute the average time for 100 runs
    priv_real=$(echo "scale=6; $priv_real / 100" | bc)
    priv_user=$(echo "scale=6; $priv_user / 100" | bc)
    priv_sys=$(echo "scale=6; $priv_sys / 100" | bc)
    pub_real=$(echo "scale=6; $pub_real / 100" | bc)
    pub_user=$(echo "scale=6; $pub_user / 100" | bc)
    pub_sys=$(echo "scale=6; $pub_sys / 100" | bc)
    
    # Append results to the output file
    echo "$curve $priv_real $priv_user $priv_sys $pub_real $pub_user $pub_sys" >> ecc_keygen_perf.dat
    
    # Clean up temporary files
    rm -f private.pem public.pem

done

echo "Performance measurement completed. Results saved in ecc_keygen_perf.dat."
