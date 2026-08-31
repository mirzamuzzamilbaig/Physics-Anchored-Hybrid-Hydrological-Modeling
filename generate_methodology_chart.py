"""
Generates a Horizontal (Landscape, 16:9 Aspect Ratio) System Architecture Flowchart
for the Lower Indus Basin Physics-Anchored Earth Observation Model (PG-MCH).
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('paper_latex/figures', exist_ok=True)
os.makedirs('paper_results/figures', exist_ok=True)

print("Generating Horizontal (Landscape) System Architecture Flowchart...")

fig, ax = plt.subplots(figsize=(16, 8.5), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

# Color Palette Tokens
C_NAVY_DARK   = '#0F172A'
C_CYAN_BG     = '#F0F9FF'
C_CYAN_BD     = '#0288D1'
C_CYAN_CARD   = '#E0F2FE'

C_EMERALD_BG  = '#ECFDF5'
C_EMERALD_BD  = '#059669'
C_EMERALD_CARD= '#D1FAE5'

C_AMBER_BG    = '#FFFBEB'
C_AMBER_BD    = '#D97706'
C_AMBER_CARD  = '#FEF3C7'

C_PURPLE_BG   = '#F5F3FF'
C_PURPLE_BD   = '#7C3AED'
C_PURPLE_CARD = '#EDE9FE'

C_SLATE_BG    = '#F8FAFC'
C_SLATE_BD    = '#334155'
C_SLATE_CARD  = '#E2E8F0'

C_ROSE_BG     = '#FFF1F2'
C_ROSE_BD     = '#E11D48'
C_ROSE_CARD   = '#FFE4E6'

def draw_arrow(ax, x1, y1, x2, y2, color='#475569', label=None, label_pos=0.5, fontsize=7.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.8, headwidth=6.5, headlength=7, shrink=0.01), zorder=5)
    if label:
        lx = x1 + (x2 - x1) * label_pos
        ly = y1 + (y2 - y1) * label_pos
        ax.text(lx, ly, label, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=color, linewidth=0.8, alpha=0.95), zorder=6)

# Main Title Header Banner
banner = patches.FancyBboxPatch((2, 90.5), 96, 7.5, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor=C_NAVY_DARK, edgecolor='none', zorder=2)
ax.add_patch(banner)
ax.text(50, 95.2, 'PHYSICS-ANCHORED HYBRID HYDROLOGICAL MODELING FRAMEWORK (PG-MCH)', ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF', zorder=3)
ax.text(50, 92.5, 'Horizontal Multi-Tier Data Processing & Dual Mass-Bounded Machine Learning Architecture', ha='center', va='center', fontsize=8.8, color='#94A3B8', zorder=3)

# -------------------------------------------------------------
# 5 HORIZONTAL STAGES (Left to Right)
# -------------------------------------------------------------

# STAGE 1: Data Ingestion (x = 2..20, y = 5..87)
st1 = patches.FancyBboxPatch((2, 5), 18, 82, boxstyle="round,pad=0.5,rounding_size=1.0", facecolor=C_CYAN_BG, edgecolor=C_CYAN_BD, linewidth=1.5, zorder=2)
ax.add_patch(st1)
ax.text(11, 83.5, 'STAGE 1\nEARTH OBSERVATION', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#0369A1', zorder=4)

# Sub-cards Stage 1
sc1_1 = patches.FancyBboxPatch((3.2, 57), 15.6, 21, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=0.8, zorder=3)
sc1_2 = patches.FancyBboxPatch((3.2, 31), 15.6, 23, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=0.8, zorder=3)
sc1_3 = patches.FancyBboxPatch((3.2, 7), 15.6, 21, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=0.8, zorder=3)
ax.add_patch(sc1_1); ax.add_patch(sc1_2); ax.add_patch(sc1_3)

ax.text(11, 74, 'Precipitation & Climate', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0369A1', zorder=4)
ax.text(11, 65, r'• CHIRPS v2.0 $P(t)$' + '\n' + r'• ERA5-Land $T_{2m}$' + '\n• ERA5 Evaporation', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(11, 49, 'Soil & Storage', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0369A1', zorder=4)
ax.text(11, 39, r'• NASA SMAP L4' + '\n' + r'• GRACE $TWSA$' + '\n• SRTM 30m DEM', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(11, 23, 'Barrage Telemetry', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#0369A1', zorder=4)
ax.text(11, 14, r'• Guddu Inflow $Q_{\mathrm{inflow}}$' + '\n• Sukkur Discharge\n• Kotri Telemetry', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)


# STAGE 2: Feature Preprocessing (x = 22..39, y = 5..87)
st2 = patches.FancyBboxPatch((22, 5), 17, 82, boxstyle="round,pad=0.5,rounding_size=1.0", facecolor=C_EMERALD_BG, edgecolor=C_EMERALD_BD, linewidth=1.5, zorder=2)
ax.add_patch(st2)
ax.text(30.5, 83.5, 'STAGE 2\nFEATURE ENGINEERING', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#047857', zorder=4)

sc2_1 = patches.FancyBboxPatch((23.2, 52), 14.6, 26, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_EMERALD_CARD, edgecolor=C_EMERALD_BD, linewidth=0.8, zorder=3)
sc2_2 = patches.FancyBboxPatch((23.2, 12), 14.6, 36, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_EMERALD_CARD, edgecolor=C_EMERALD_BD, linewidth=0.8, zorder=3)
ax.add_patch(sc2_1); ax.add_patch(sc2_2)

ax.text(30.5, 73, 'Antecedent Memory', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#047857', zorder=4)
ax.text(30.5, 61, r'$API_t = \gamma P_{t-1} + \gamma^2 P_{t-2}$' + '\n' + r'($\gamma = 0.60$ strictly lagged)' + '\nSoil saturation memory', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(30.5, 41, 'Atmospheric Deficit', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#047857', zorder=4)
ax.text(30.5, 26, r'$D_{\mathrm{deficit}} = PET - P$' + '\nMonthly aggregation\nGEE Spatial Masking\n140,914 km² Sindh', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)


# STAGE 3: Physics-Anchored Core (x = 41..61, y = 5..87)
st3 = patches.FancyBboxPatch((41, 5), 20, 82, boxstyle="round,pad=0.5,rounding_size=1.0", facecolor=C_AMBER_BG, edgecolor=C_AMBER_BD, linewidth=1.5, zorder=2)
ax.add_patch(st3)
ax.text(51, 83.5, 'STAGE 3\nPHYSICS-ANCHORED CORE', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#B45309', zorder=4)

sc3_1 = patches.FancyBboxPatch((42.2, 47), 17.6, 31, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_AMBER_CARD, edgecolor=C_AMBER_BD, linewidth=0.8, zorder=3)
sc3_2 = patches.FancyBboxPatch((42.2, 9), 17.6, 34, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_PURPLE_CARD, edgecolor=C_PURPLE_BD, linewidth=0.8, zorder=3)
ax.add_patch(sc3_1); ax.add_patch(sc3_2)

ax.text(51, 73, 'Physical Baseline (NNLS)', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#B45309', zorder=4)
ax.text(51, 59, r'$Q_{\mathrm{base}} = \beta_0 + \beta_1 P +$' + '\n' + r'$\beta_2 API + \beta_3 Q_{\mathrm{inflow}}$' + '\n' + r'Non-Negative ($\beta \geq 0$)' + '\n' + r'L2 Penalty ($\lambda=2.0$)', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(51, 38, 'Residual GBDT Ensemble', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#6D28D9', zorder=4)
ax.text(51, 23, r'$\varepsilon(t) = Q_{\mathrm{obs}} - Q_{\mathrm{base}}$' + '\n' + r'$\hat{\varepsilon}(t) = \mathcal{F}_{\mathrm{trees}}(X)$' + '\nCaptures non-linearities\n' + r'$N=240$ mo. calibration', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)


# STAGE 4: Dual Mass-Bounded Output (x = 63..80, y = 5..87)
st4 = patches.FancyBboxPatch((63, 5), 17, 82, boxstyle="round,pad=0.5,rounding_size=1.0", facecolor=C_SLATE_BG, edgecolor=C_SLATE_BD, linewidth=1.5, zorder=2)
ax.add_patch(st4)
ax.text(71.5, 83.5, 'STAGE 4\nMASS-BOUNDED OUTPUT', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#334155', zorder=4)

sc4_1 = patches.FancyBboxPatch((64.2, 45), 14.6, 33, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_SLATE_CARD, edgecolor=C_SLATE_BD, linewidth=0.8, zorder=3)
sc4_2 = patches.FancyBboxPatch((64.2, 9), 14.6, 32, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_SLATE_CARD, edgecolor=C_SLATE_BD, linewidth=0.8, zorder=3)
ax.add_patch(sc4_1); ax.add_patch(sc4_2)

ax.text(71.5, 73, 'Mass-Balance Envelope', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#334155', zorder=4)
ax.text(71.5, 58, r'$W_{\mathrm{total}} = P(t) +$' + '\n' + r'$Q_{\mathrm{inflow}}(t) + API_t$' + '\nUpper Mass Bound\nZero Floor Bound', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(71.5, 36, 'Composite Runoff', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#334155', zorder=4)
ax.text(71.5, 21, r'$\hat{Q} = \min(W_{\mathrm{total}},$' + '\n' + r'$\max(0, Q_{\mathrm{base}} + \hat{\varepsilon}))$' + '\nEliminates unphysical\nOOD extrapolation', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)


# STAGE 5: Evaluation & Applications (x = 82..98, y = 5..87)
st5 = patches.FancyBboxPatch((82, 5), 16, 82, boxstyle="round,pad=0.5,rounding_size=1.0", facecolor=C_ROSE_BG, edgecolor=C_ROSE_BD, linewidth=1.5, zorder=2)
ax.add_patch(st5)
ax.text(90, 83.5, 'STAGE 5\nEVALUATION & APP', ha='center', va='center', fontsize=8.5, fontweight='bold', color='#BE123C', zorder=4)

sc5_1 = patches.FancyBboxPatch((83.1, 47), 13.8, 31, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_ROSE_CARD, edgecolor=C_ROSE_BD, linewidth=0.8, zorder=3)
sc5_2 = patches.FancyBboxPatch((83.1, 9), 13.8, 34, boxstyle="round,pad=0.3,rounding_size=0.5", facecolor=C_ROSE_CARD, edgecolor=C_ROSE_BD, linewidth=0.8, zorder=3)
ax.add_patch(sc5_1); ax.add_patch(sc5_2)

ax.text(90, 73, 'Holdout Validation', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#BE123C', zorder=4)
ax.text(90, 59, '• 2022 Mega-Flood\n  KGE = 0.812\n  FHV = -4.0%\n• 2020-2024 Test\n  KGE = 0.895', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

ax.text(90, 38, 'Decision Support', ha='center', va='center', fontsize=7.8, fontweight='bold', color='#BE123C', zorder=4)
ax.text(90, 23, '• Guddu-Sukkur-Kotri\n  1-3 mo Forecasts\n• Manchar Retention\n• Delta Outflows', ha='center', va='center', fontsize=7.2, color='#1E293B', zorder=4)

# -------------------------------------------------------------
# CONNECTING ARROWS BETWEEN STAGES
# -------------------------------------------------------------
draw_arrow(ax, 20, 46, 22, 46, color='#0288D1')
draw_arrow(ax, 39, 46, 41, 46, color='#059669')
draw_arrow(ax, 61, 46, 63, 46, color='#D97706')
draw_arrow(ax, 80, 46, 82, 46, color='#334155')

fig.savefig('paper_latex/figures/Figure_Methodology_Hierarchical_Framework.png', dpi=300, bbox_inches='tight')
fig.savefig('paper_results/figures/Figure_Methodology_Hierarchical_Framework.png', dpi=300, bbox_inches='tight')
print("Successfully generated HORIZONTAL (Landscape, 16:9) System Architecture Flowchart!")
