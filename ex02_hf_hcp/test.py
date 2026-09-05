import numpy as np
from ase.build import bulk
from ase.io import write

# 1. Hf 실험값 격자상수(a ≈ 3.196 Å) 기준 스위프 범위 설정
c_over_a = 1.58
a_vals = np.linspace(3.05, 3.35, 7)

# 2. Quantum ESPRESSO 계산 파라미터 블록
input_data = {
    'control': {
        'calculation': 'scf',
        'restart_mode': 'from_scratch',
        'pseudo_dir': '../pseudo',
        'tprnfor': True,
        'tstress': True,
    },
    'system': {
        'ecutwfc': 50.0,
        'ecutrho': 400.0,
        'occupations': 'smearing',
        'smearing': 'mv',
        'degauss': 0.02,
    },
    'electrons': {
        'conv_thr': 1.0e-8,
        'mixing_beta': 0.7,
    }
}

# 3. 의사퍼텐셜 파일 연결
pseudopotentials = {'Hf': 'Hf.pbe-spn-kjpaw_psl.1.0.0.UPF'}

# 4. 반복문으로 각 격자 크기별 .in 파일 자동 생성
for a in a_vals:
    c = a * c_over_a
    atoms = bulk('Hf', 'hcp', a=a, c=c)
    
    input_data['control']['outdir'] = f'./tmp_{a:.3f}'
    input_data['control']['prefix'] = f'hf_{a:.3f}'
    
    filename = f'hf_a_{a:.3f}.in'
    write(filename, atoms, format='espresso-in',
          input_data=input_data,
          pseudopotentials=pseudopotentials,
          kpts=(8, 8, 6))
    print(f"생성 완료: {filename} (a = {a:.3f} Å, c = {c:.3f} Å)")

print("모든 입력 파일 생성이 완료되었습니다.")