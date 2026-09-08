import numpy as np
import matplotlib.pyplot as plt

k_list = [4, 6, 8, 10, 12]
energies_ry = []

for k in k_list:
    fname = f"kpt_{k}.out"
    e_ry = None
    try:
        with open(fname, 'r') as f:
            for line in f:
                if '!' in line and 'total energy' in line:
                    parts = line.split('=')
                    e_ry = float(parts[1].replace('Ry', '').strip())
    except FileNotFoundError:
        print(f"파일 없음: {fname}")
        
    if e_ry is not None:
        energies_ry.append(e_ry)
    else:
        print(f"경고: {fname}에서 에너지를 찾지 못했습니다.")

energies_ry = np.array(energies_ry)
energies_ev = energies_ry * 13.6056980659
nat = 2

e_per_atom_ev = energies_ev / nat
delta_e_mev = np.zeros(len(k_list))
if len(energies_ry) == len(k_list):
    delta_e_mev[1:] = np.abs(e_per_atom_ev[1:] - e_per_atom_ev[:-1]) * 1000.0

print('=' * 64)
print(f"{'k-grid':^12} | {'Total Energy (Ry)':^18} | {'ΔE/atom (meV)':^15} | {'수렴 여부 (<1 meV)':^12}")
print('=' * 64)

conv_k = None
for i, k in enumerate(k_list):
    if i == 0:
        status = '-'
    else:
        is_conv = delta_e_mev[i] < 1.0
        status = '수렴 (Pass)' if is_conv else '미달 (Fail)'
        if is_conv and conv_k is None:
            conv_k = f"{k}x{k}x{k}"
    print(f"{f'{k}x{k}x{k}':^12} | {energies_ry[i]:^18.6f} | {delta_e_mev[i]:^15.3f} | {status:^12}")

print('=' * 64)
if conv_k:
    print(f"추천 최적 k-grid: {conv_k} (기준: ΔE/atom < 1 meV)")
print('=' * 64)

fig, ax1 = plt.subplots(figsize=(7, 5), dpi=150)
color = 'tab:blue'
ax1.set_xlabel('k-point Grid (N x N x N)', fontsize=11)
ax1.set_ylabel('Total Energy (Ry)', color=color, fontsize=11)
ax1.plot(k_list, energies_ry, marker='o', color=color, linewidth=2, label='Total Energy')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True, linestyle=':', alpha=0.6)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('|ΔE / atom| (meV)', color=color, fontsize=11)
ax2.plot(k_list[1:], delta_e_mev[1:], marker='s', linestyle='--', color=color, linewidth=2, label='|ΔE/atom|')
ax2.axhline(1.0, color='gray', linestyle=':', label='1 meV/atom Threshold')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('ScAl (CsCl) k-point Convergence Test', fontsize=13)
fig.tight_layout()
plt.savefig('scal_kpt_convergence.png')
print("수렴 그래프가 'scal_kpt_convergence.png'로 저장되었습니다.")
