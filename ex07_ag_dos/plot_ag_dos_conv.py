import numpy as np
import matplotlib.pyplot as plt

k_list = [4, 8, 12, 16]
energies_ry = []
fermi_energies = []

# 1. Total Energy & Fermi Level 파싱
for k in k_list:
    scf_out = f"ag_scf_k{k}.out"
    e_ry = None
    ef = None
    with open(scf_out, 'r') as f:
        for line in f:
            if '!' in line and 'total energy' in line:
                parts = line.split('=')
                e_ry = float(parts[1].replace('Ry', '').strip())
            if 'the Fermi energy is' in line:
                ef = float(line.split('is')[1].replace('ev', '').replace('eV', '').strip())
    energies_ry.append(e_ry)
    fermi_energies.append(ef)

energies_ry = np.array(energies_ry)
# FCC 원시 셀 nat=1이므로 그대로 1원자당 에너지
energies_ev = energies_ry * 13.6056980659
delta_e_mev = np.zeros(len(k_list))
delta_e_mev[1:] = np.abs(energies_ev[1:] - energies_ev[:-1]) * 1000.0

print("=" * 65)
print(f"{'k-grid':^10} | {'Total Energy (Ry)':^18} | {'ΔE (meV/atom)':^15} | {'E_F (eV)':^10}")
print("=" * 65)
for i, k in enumerate(k_list):
    d_str = '-' if i == 0 else f"{delta_e_mev[i]:.3f}"
    print(f"{f'{k}x{k}x{k}':^10} | {energies_ry[i]:^18.6f} | {d_str:^15} | {fermi_energies[i]:^10.4f}")
print("=" * 65)

# 2. DOS 곡선 비교 플롯 생성
plt.figure(figsize=(9, 5.5), dpi=150)
colors = ['gray', 'tab:green', 'tab:blue', 'tab:red']
styles = [':', '--', '-.', '-']

for i, k in enumerate(k_list):
    dos_file = f"ag_k{k}.dos"
    data = np.loadtxt(dos_file, comments='#')
    energy = data[:, 0]
    dos = data[:, 1]
    ef = fermi_energies[i]
    
    # E - E_F 기준으로 정렬하여 페르미 에너지를 0 eV에 맞춤
    plt.plot(energy - ef, dos, label=f"{k}x{k}x{k}", color=colors[i], linestyle=styles[i], linewidth=1.8 if k==16 else 1.2)

plt.axvline(0, color='black', linestyle='--', linewidth=1.0, label='Fermi Level (E_F)')
plt.xlim(-8, 5)
plt.ylim(0, 3.5)
plt.xlabel('Energy - E_F (eV)', fontsize=12)
plt.ylabel('DOS (states/eV/atom)', fontsize=12)
plt.title('FCC Ag Electronic DOS Convergence with k-point Grids', fontsize=13)
plt.legend(loc='upper right', frameon=True)
plt.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig('ag_dos_convergence.png')
print("DOS 수렴 비교 그래프가 'ag_dos_convergence.png'로 저장되었습니다.")
