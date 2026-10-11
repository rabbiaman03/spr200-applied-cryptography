# Lab 4 — ECC Key Generation and Signing Performance

**Author:** Rabbi Muhammad Aman · **Course:** SPR200 (Winter 2025)

## Objective
Measure how the choice of elliptic curve and hash function affects performance, using OpenSSL and the `time` command, with each result averaged over 100 runs.

## Method
- [`measure_ecc_key_generation.sh`](measure_ecc_key_generation.sh) generates private and public keys on **secp256k1, prime256v1, secp384r1 and brainpoolP512t1**, recording real, user and system time.
- [`measure_signing_performance.sh`](measure_signing_performance.sh) signs a 100 MB random file with a secp256k1 key using **SHA3-256, SHA3-512 and RIPEMD-160**.
- The gnuplot scripts ([`plot_ecc_keygen_perf_bonus.gnu`](plot_ecc_keygen_perf_bonus.gnu), [`plot_signing_performence.gnu`](plot_signing_performence.gnu)) produce the charts.

## Results

![ECC key generation](ecc_keygen_performance.png)

![Signing performance](signing_performance.png)

| Hash | Average time to sign 100 MB (s) |
|---|---|
| SHA3-256 | 0.192 |
| RIPEMD-160 | 0.326 |
| SHA3-512 | 0.364 |

Raw data: [`ecc_keygen_perf.dat`](ecc_keygen_perf.dat), [`signing_performance.dat`](signing_performance.dat)

## Takeaways
- Signing time for a large file is dominated by hashing. SHA3-256 was about 1.9× faster than SHA3-512 here.
- Key generation on all of these curves takes milliseconds, so curve choice depends on the security level and ecosystem support rather than speed.

## Reproduce
```bash
bash measure_ecc_key_generation.sh && gnuplot plot_ecc_keygen_perf_bonus.gnu
bash measure_signing_performance.sh && gnuplot plot_signing_performence.gnu
```
