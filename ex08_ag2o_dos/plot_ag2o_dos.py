import numpy as np
import matplotlib.pyplot as plt

# 1. Fermi Energy 추출
ef = None
with open("ag2o_scf.out", "r") as f:
    for line in f:
        if "the Fermi energy is" in line:
            ef = float(line.split("is")[1].replace("ev", "").replace("eV", "").strip())
            break

print(f"Fermi Energy (E_F): {ef:.4f} eV")

# 2. DOS 데이터 로드
data = np.loadtxt("ag2o.dos", comments="#")
energy = data[:, 0]
dos = data[:, 1]

# 페르미 준위에서의 DOS 값 근사 (E - E_F ≈ 0)
idx_ef = np.argmin(np.abs(energy - ef))
dos_at_ef = dos[idx_ef]
print(f"DOS at Fermi Level: {dos_at_ef:.4f} states/eV/cell")

if dos_at_ef > 0.05:
    print(">> 판정: 페르미 준위에서 DOS > 0 이므로 DFT는 Ag2O를 [금속(Metal)]으로 예측함!")
else:
    print(">> 판정: 페르미 준위 주변에 밴드갭이 존재하여 [반도체/절연체]로 예측함!")

# 3. 플롯 생성
plt.figure(figsize=(8, 5), dpi=150)
plt.plot(energy - ef, dos, color='crimson', linewidth=1.8, label=r'Bulk $\mathrm{Ag_2O}$ DOS')
plt.axvline(0, color='black', linestyle='--', linewidth=1.2, label='Fermi Level ($E_F$)')
plt.xlim(-8, 6)
plt.ylim(0, max(dos[np.abs(energy - ef) < 8]) * 1.1)
plt.xlabel(r'Energy - $E_F$ (eV)', fontsize=12)
plt.ylabel('DOS (states / eV / cell)', fontsize=12)
plt.title(r'Electronic DOS of Bulk $\mathrm{Ag_2O}$ (PBE Functional)', fontsize=13)
plt.legend(frameon=True, loc='upper right')
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig('ag2o_dos.png')
print("그래프가 'ag2o_dos.png'로 저장되었습니다.")
