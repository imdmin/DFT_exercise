import glob
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read
from ase.eos import EquationOfState

# 1. 계산된 모든 .out 파일 로드 및 정렬
out_files = sorted(glob.glob('hf_a_*.out'))
if not out_files:
    raise FileNotFoundError("hf_a_*.out 결과 파일을 찾을 수 없습니다.")

volumes = []
energies = []

for f in out_files:
    # ASE의 read 함수로 QE 출력 파일에서 최종 구조와 에너지 자동 추출
    atoms = read(f, format='espresso-out')
    volumes.append(atoms.get_volume())          # 단위 격자 부피 (Å^3)
    energies.append(atoms.get_potential_energy()) # 총에너지 (eV 단위로 자동 변환됨)

volumes = np.array(volumes)
energies = np.array(energies)

# 2. Birch-Murnaghan 상태방정식 피팅
# eos='birchmurnaghan' 적용 (3차 BM 식)
eos = EquationOfState(volumes, energies, eos='birchmurnaghan')
v0, e0, B = eos.fit()

# 체적탄성률 단위 변환 (eV/Å^3 -> GPa)
# 1 eV/Å^3 ≈ 160.21766208 GPa
B_GPa = B / 0.006241509

# 3. 최적 격자상수 a0, c0 계산 (c/a = 1.58 고정 조건)
# HCP 단위 격자 부피 식: V = (sqrt(3)/2) * a^2 * c = (sqrt(3)/2) * 1.58 * a^3
c_over_a = 1.58
a0 = (v0 / ((np.sqrt(3) / 2.0) * c_over_a)) ** (1.0 / 3.0)
c0 = a0 * c_over_a

# 4. 결과 출력 및 실험값 비교
a_exp = 3.196
c_exp = 5.051
B_exp = 110.0  # 실험 체적탄성률 약 108~112 GPa

print("=" * 50)
print("       Hf HCP Birch-Murnaghan 피팅 결과")
print("=" * 50)
print(f"평형 부피 (V0)        : {v0:.4f} Å^3")
print(f"바닥 상태 에너지 (E0) : {e0:.6f} eV")
print(f"체적탄성률 (B0)       : {B_GPa:.2f} GPa (실험값: ~{B_exp:.1f} GPa)")
print("-" * 50)
print(f"계산된 a0 : {a0:.4f} Å  |  실험값: {a_exp:.4f} Å  (오차: {abs(a0 - a_exp)/a_exp * 100:.2f}%)")
print(f"계산된 c0 : {c0:.4f} Å  |  실험값: {c_exp:.4f} Å  (오차: {abs(c0 - c_exp)/c_exp * 100:.2f}%)")
print("=" * 50)

# 5. 상태방정식 피팅 곡선 그래프 저장
eos.plot('hf_eos_fitting.png')
print("피팅 그래프가 'hf_eos_fitting.png'로 저장되었습니다.")