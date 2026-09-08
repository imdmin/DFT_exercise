#!/bin/bash
export OMP_NUM_THREADS=1

for k in 4 8 12 16; do
    echo "=== [k-grid: ${k}x${k}x${k}] 계산 시작 ==="
    
    # 1. SCF 연산 (총에너지)
    mpirun -np 2 pw.x < "ag_scf_k${k}.in" > "ag_scf_k${k}.out"
    
    # 2. DOS 연산
    dos.x < "ag_dos_k${k}.in" > "ag_dos_k${k}.out"
    
    echo "=== [k-grid: ${k}x${k}x${k}] 완료! ==="
done
