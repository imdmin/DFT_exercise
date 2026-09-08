import re
import numpy as np
import matplotlib.pyplot as plt

ecut_list = [30, 40, 50, 60, 70, 80]
energies_ry = []

for ecut in ecut_list:
    fname = f"ecut_{ecut}.out"
    e_ry = None
    with open(fname, 'r') as f:
        for line in f:
            if "!" in line and "total energy" in line:
                parts = line.split('=')
                e_ry = float(parts[1].replace('Ry', '').strip())
    if e_ry is not None:
        energies_ry.append(e_ry)
    else:
        print(f"경고: {fname}에서 에너지를 찾을 수 없습니다.")

energies_ry = np.array(energies_ry)
# 단위 변환: 1 Ry = 13.605698 eV, 1 eV = 1000 meV
energies_ev = energies_ry * 13.6056980659
nat = 2  # ScAl 단위격자 내 원자 수 (Sc: 1, Al: 1)

# 원자당 에너지 (eV/atom)
e_per_atom_ev = energies_ev / nat

# 연속된 ecut 간 원자당 에너지 차이 (meV/atom)
delta_e_mev = np.zeros(len(ecut_list))
delta_e_mev[1:] = np.abs(e_per_atom_ev[1:] - e_per_atom_ev[:-1]) * 1000.0

print("=" * 64)
print(f"{'ecutwfc (Ry)':^12} | {'Total Energy (Ry)':^18} | {'ΔE/atom (meV)':^15} | {'수렴 여부 (<1 meV)':^12}")
print("=" * 64)

conv_ecut = None
for i, ecut in enumerate(ecut_list):
    if i == 0:
        status = "-"
    else:
        is_conv = delta_e_mev[i] < 1.0
        status = "수렴 (Pass)" if is_conv else "미달 (Fail)"
        if is_conv and conv_ecut is None:
            conv_ecut = ecut
    print(f"{ecut:^12} | {energies_ry[i]:^18.6f} | {delta_e_mev[i]:^15.3f} | {status:^12}")

print("=" * 64)
if conv_ecut:
    print(f"추천 최적 ecutwfc: {conv_ecut} Ry (기준: ΔE/atom < 1 meV)")
print("=" * 64)

# 수렴 그래프 시각화
fig, ax1 = plt.subplots(figsize=(7, 5), dpi=150)

color = 'tab:blue'
ax1.set_xlabel('ecutwfc (Ry)', fontsize=11)
ax1.set_ylabel('Total Energy (Ry)', color=color, fontsize=11)
ax1.plot(ecut_list, energies_ry, marker='o', color=color, linewidth=2, label='Total Energy')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('|ΔE / atom| (meV)', color=color, fontsize=11)
ax2.plot(ecut_list[1:], delta_e_mev[1:], marker='s', linestyle='--', color=color, linewidth=2, label='|ΔE/atom|')
ax2.axhline(1.0, color='gray', linestyle=':', label='1 meV/atom Threshold')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('ScAl (CsCl) ecutwfc Convergence Test', fontsize=13)
fig.tight_layout()
plt.savefig('scal_ecut_convergence.png')
print("수렴 그래프가 'scal_ecut_convergence.png'로 저장되었습니다.")
