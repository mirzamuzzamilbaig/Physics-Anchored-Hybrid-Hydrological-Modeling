"""
Generates a State-of-the-Art, Nature/IEEE-Grade System Architecture Diagram
for the Lower Indus Basin Physics-Anchored Earth Observation Model (PG-MCH).

Visual Palette & Design System:
- Professional Dark Slate / Navy / Emerald / Cyan / Amber / Rose Palette
- Multi-tier Modular Sub-card Layout with Dataflow Annotations
- Dedicated Mathematical Formula Badges & High-Contrast Containers
- 300 DPI High-Resolution Output for Nature / IEEE / AGU Manuscripts
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

os.makedirs('paper_latex/figures', exist_ok=True)
os.makedirs('paper_results/figures', exist_ok=True)

print("Generating Nature/IEEE-Grade System Architecture Flowchart...")

fig, ax = plt.subplots(figsize=(14, 16), dpi=300)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')
fig.patch.set_facecolor('#FFFFFF')

# Color Palette Tokens
C_NAVY_DARK   = '#0F172A'  # Header Banner & Outer Accents
C_CYAN_BG     = '#F0F9FF'  # Layer 1: Data Ingestion
C_CYAN_BD     = '#0288D1'
C_CYAN_CARD   = '#E0F2FE'

C_EMERALD_BG  = '#ECFDF5'  # Layer 2: Feature Engineering
C_EMERALD_BD  = '#059669'
C_EMERALD_CARD= '#D1FAE5'

C_AMBER_BG    = '#FFFBEB'  # Layer 3A: Physical Water Balance
C_AMBER_BD    = '#D97706'
C_AMBER_CARD  = '#FEF3C7'

C_PURPLE_BG   = '#F5F3FF'  # Layer 3B: Residual GBDT
C_PURPLE_BD   = '#7C3AED'
C_PURPLE_CARD = '#EDE9FE'

C_SLATE_BG    = '#F8FAFC'  # Layer 4: Mass-Bounded Output
C_SLATE_BD    = '#334155'
C_SLATE_CARD  = '#E2E8F0'

C_ROSE_BG     = '#FFF1F2'  # Layer 5: Validation & Applications
C_ROSE_BD     = '#E11D48'
C_ROSE_CARD   = '#FFE4E6'

def draw_arrow(ax, x1, y1, x2, y2, color='#475569', label=None, label_pos=0.5, fontsize=8):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(facecolor=color, edgecolor=color, width=1.6, headwidth=6.5, headlength=7, shrink=0.015), zorder=5)
    if label:
        lx = x1 + (x2 - x1) * label_pos
        ly = y1 + (y2 - y1) * label_pos
        ax.text(lx, ly, label, ha='center', va='center', fontsize=fontsize, fontweight='bold', color=color,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor=color, linewidth=0.8, alpha=0.95), zorder=6)

# Main Title Header Banner
banner = patches.FancyBboxPatch((3, 93.5), 94, 5.5, boxstyle="round,pad=0.4,rounding_size=0.8",
                                facecolor='#0F172A', edgecolor='none', zorder=2)
ax.add_patch(banner)
ax.text(50, 96.6, 'PHYSICS-ANCHORED HYBRID HYDROLOGICAL MODELING FRAMEWORK (PG-MCH)', ha='center', va='center', fontsize=12, fontweight='bold', color='#FFFFFF', zorder=3)
ax.text(50, 94.6, 'Cloud-Native Earth Observation & Dual Mass-Bounded Machine Learning in Data-Sparse Alluvial Basins', ha='center', va='center', fontsize=8.8, color='#94A3B8', zorder=3)

# -------------------------------------------------------------
# LAYER 1: Earth Observation & Telemetry Ingestion (Data Layer)
# -------------------------------------------------------------
l1_bg = patches.FancyBboxPatch((3, 80.0), 94, 12.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                               facecolor=C_CYAN_BG, edgecolor=C_CYAN_BD, linewidth=1.8, zorder=2)
ax.add_patch(l1_bg)

# Layer 1 Ribbon
t1_box = patches.FancyBboxPatch((5, 89.2), 90, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                facecolor=C_CYAN_BD, edgecolor='none', zorder=3)
ax.add_patch(t1_box)
ax.text(50, 90.45, 'LAYER 1: CLOUD-NATIVE EARTH OBSERVATION & TELEMETRY INGESTION (GOOGLE EARTH ENGINE)', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)

# Layer 1 Sub-cards (3 Columns)
sub1_1 = patches.FancyBboxPatch((5, 81.0), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=1.0, zorder=3)
sub1_2 = patches.FancyBboxPatch((35.75, 81.0), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=1.0, zorder=3)
sub1_3 = patches.FancyBboxPatch((66.5, 81.0), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_CYAN_CARD, edgecolor=C_CYAN_BD, linewidth=1.0, zorder=3)
ax.add_patch(sub1_1); ax.add_patch(sub1_2); ax.add_patch(sub1_3)

ax.text(19.25, 86.8, 'ATMOSPHERIC FORCING', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0369A1', zorder=4)
ax.text(19.25, 83.9, r'• CHIRPS v2.0 Precip $P(t)$ ($0.05^\circ$)' + '\n' + r'• ERA5-Land $T_{2m}$ & $ET(t)$ ($0.1^\circ$)', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(50.0, 86.8, 'TERRESTRIAL & SOIL STORAGE', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0369A1', zorder=4)
ax.text(50.0, 83.9, r'• NASA SMAP L4 Moisture (9km)' + '\n' + r'• GRACE / GRACE-FO Mascons ($TWSA$)', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(80.75, 86.8, 'HYDRAULIC & BOUNDARY', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#0369A1', zorder=4)
ax.text(80.75, 83.9, r'• SRTM 30m Digital Elevation Model' + '\n' + r'• Guddu Telemetry $Q_{\mathrm{inflow}}(t)$', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

# Connector Arrow: Layer 1 -> Layer 2
draw_arrow(ax, 50, 80.0, 50, 76.5, color='#0288D1', label=r"Multi-Source Geospatial Inputs $\mathbf{X}_{\mathrm{raw}}(t)$", fontsize=7.8)

# -------------------------------------------------------------
# LAYER 2: Feature Engineering & Preprocessing
# -------------------------------------------------------------
l2_bg = patches.FancyBboxPatch((3, 64.5), 94, 12.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                               facecolor=C_EMERALD_BG, edgecolor=C_EMERALD_BD, linewidth=1.8, zorder=2)
ax.add_patch(l2_bg)

t2_box = patches.FancyBboxPatch((5, 73.7), 90, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                facecolor=C_EMERALD_BD, edgecolor='none', zorder=3)
ax.add_patch(t2_box)
ax.text(50, 74.95, 'LAYER 2: HYDRO-CLIMATIC FEATURE ENGINEERING & SPATIAL HARMONIZATION', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)

# Layer 2 Sub-cards (3 Columns)
sub2_1 = patches.FancyBboxPatch((5, 65.5), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_EMERALD_CARD, edgecolor=C_EMERALD_BD, linewidth=1.0, zorder=3)
sub2_2 = patches.FancyBboxPatch((35.75, 65.5), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_EMERALD_CARD, edgecolor=C_EMERALD_BD, linewidth=1.0, zorder=3)
sub2_3 = patches.FancyBboxPatch((66.5, 65.5), 28.5, 7.3, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_EMERALD_CARD, edgecolor=C_EMERALD_BD, linewidth=1.0, zorder=3)
ax.add_patch(sub2_1); ax.add_patch(sub2_2); ax.add_patch(sub2_3)

ax.text(19.25, 71.3, 'SPATIAL BOUNDARIES', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#047857', zorder=4)
ax.text(19.25, 68.4, r'• Lower Indus Basin ($140,914\text{ km}^2$)' + '\n' + r'• Guddu, Sukkur, Kotri & Manchar', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(50.0, 71.3, 'SOIL MOISTURE MEMORY', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#047857', zorder=4)
ax.text(50.0, 68.4, r'$API_t = P_t + \gamma P_{t-1} + \gamma^2 P_{t-2}$' + '\n' + r'(Calibrated decay $\gamma = 0.60$)', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(80.75, 71.3, 'DEFICIT & HOLDOUT SPLIT', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#047857', zorder=4)
ax.text(80.75, 68.4, r'• $D_{\mathrm{deficit}}(t) = PET(t) - P(t)$' + '\n' + r'• Zero-Lookahead Holdout Split', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

# Connector Arrows down to Layer 3A and 3B
draw_arrow(ax, 26, 64.5, 26, 59.5, color='#059669', label=r"$\mathbf{X}_{\mathrm{phys}}$", fontsize=7.8)
draw_arrow(ax, 74, 64.5, 74, 59.5, color='#059669', label=r"$\mathbf{X}_{\mathrm{res}}$", fontsize=7.8)

# -------------------------------------------------------------
# LAYER 3A & 3B: Parallel Physics & ML Ensemble Architecture
# -------------------------------------------------------------
# Layer 3A Container (Left)
l3a_bg = patches.FancyBboxPatch((3, 40.0), 45, 19.5, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=C_AMBER_BG, edgecolor=C_AMBER_BD, linewidth=1.8, zorder=2)
ax.add_patch(l3a_bg)

t3a_box = patches.FancyBboxPatch((5, 56.2), 41, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                 facecolor=C_AMBER_BD, edgecolor='none', zorder=3)
ax.add_patch(t3a_box)
ax.text(25.5, 57.45, 'LAYER 3A: PHYSICAL WATER BALANCE', ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF', zorder=4)

# Formula Box 3A
f3a_box = patches.FancyBboxPatch((5, 49.0), 41, 6.2, boxstyle="round,pad=0.3,rounding_size=0.6",
                                 facecolor=C_AMBER_CARD, edgecolor=C_AMBER_BD, linewidth=1.0, zorder=3)
ax.add_patch(f3a_box)
ax.text(25.5, 53.4, r'Linear Water Balance Baseline:', ha='center', va='center', fontsize=8.0, fontweight='bold', color='#B45309', zorder=4)
ax.text(25.5, 50.8, r'$Q_{\mathrm{base}}(t) = \beta_0 + \beta_1 P(t) + \beta_2 API(t) + \beta_3 Q_{\mathrm{inflow}}(t)$', ha='center', va='center', fontsize=8.0, color='#1E293B', zorder=4)

# Optimization Box 3A
opt3a_box = patches.FancyBboxPatch((5, 41.0), 41, 7.0, boxstyle="round,pad=0.3,rounding_size=0.6",
                                   facecolor='#FFFFFF', edgecolor=C_AMBER_BD, linewidth=1.0, zorder=3)
ax.add_patch(opt3a_box)
ax.text(25.5, 46.2, r'Non-Negative Regularization (NNLS):', ha='center', va='center', fontsize=8.0, fontweight='bold', color='#B45309', zorder=4)
ax.text(25.5, 44.0, r'$\boldsymbol{\beta} = \arg\min_{\boldsymbol{\beta} \geq 0} \| y - X\boldsymbol{\beta} \|_2^2 + \lambda \|\boldsymbol{\beta}\|_2^2 \quad (\lambda = 2.0)$', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)
ax.text(25.5, 42.0, r'✓ Guarantees Monotonic Mass Scaling Without Collapse', ha='center', va='center', fontsize=7.3, fontweight='bold', color='#047857', zorder=4)

# Layer 3B Container (Right)
l3b_bg = patches.FancyBboxPatch((52, 40.0), 45, 19.5, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=C_PURPLE_BG, edgecolor=C_PURPLE_BD, linewidth=1.8, zorder=2)
ax.add_patch(l3b_bg)

t3b_box = patches.FancyBboxPatch((54, 56.2), 41, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                 facecolor=C_PURPLE_BD, edgecolor='none', zorder=3)
ax.add_patch(t3b_box)
ax.text(74.5, 57.45, 'LAYER 3B: RESIDUAL GBDT ENSEMBLE', ha='center', va='center', fontsize=9.2, fontweight='bold', color='#FFFFFF', zorder=4)

# Formula Box 3B
f3b_box = patches.FancyBboxPatch((54, 49.0), 41, 6.2, boxstyle="round,pad=0.3,rounding_size=0.6",
                                 facecolor=C_PURPLE_CARD, edgecolor=C_PURPLE_BD, linewidth=1.0, zorder=3)
ax.add_patch(f3b_box)
ax.text(74.5, 53.4, r'Residual Target Modeling:', ha='center', va='center', fontsize=8.0, fontweight='bold', color='#6D28D9', zorder=4)
ax.text(74.5, 50.8, r'$\varepsilon(t) = Q_{\mathrm{obs}}(t) - Q_{\mathrm{base}}(t)$', ha='center', va='center', fontsize=8.2, color='#1E293B', zorder=4)

# ML Box 3B
ml3b_box = patches.FancyBboxPatch((54, 41.0), 41, 7.0, boxstyle="round,pad=0.3,rounding_size=0.6",
                                  facecolor='#FFFFFF', edgecolor=C_PURPLE_BD, linewidth=1.0, zorder=3)
ax.add_patch(ml3b_box)
ax.text(74.5, 46.2, r'Non-Linear Decision Tree Ensemble:', ha='center', va='center', fontsize=8.0, fontweight='bold', color='#6D28D9', zorder=4)
ax.text(74.5, 44.0, r'$\hat{\varepsilon}(t) = \mathcal{F}_{\mathrm{trees}}(P, Q_{\mathrm{inflow}}, ET, T_{2m}, D_{\mathrm{def}}, API, \mathrm{Month})$', ha='center', va='center', fontsize=7.6, color='#1E293B', zorder=4)
ax.text(74.5, 42.0, r'✓ Captures Non-Stationary Hydrodynamic Storage Deviations', ha='center', va='center', fontsize=7.3, fontweight='bold', color='#6D28D9', zorder=4)

# Connectors to Merger Node
draw_arrow(ax, 25.5, 40.0, 47.2, 34.5, color='#D97706', label=r"$Q_{\mathrm{base}}$", fontsize=7.8)
draw_arrow(ax, 74.5, 40.0, 52.8, 34.5, color='#7C3AED', label=r"$\hat{\varepsilon}$", fontsize=7.8)

# Merger Node Circle
merge_badge = patches.Circle((50, 33.5), radius=2.0, facecolor='#0F172A', edgecolor='white', linewidth=1.5, zorder=6)
ax.add_patch(merge_badge)
ax.text(50, 33.5, '+', ha='center', va='center', fontsize=14, fontweight='bold', color='white', zorder=7)

draw_arrow(ax, 50, 31.5, 50, 27.5, color='#0F172A', label=r"Unconstrained Composite $Q_{\mathrm{base}} + \hat{\varepsilon}$", fontsize=7.5)

# -------------------------------------------------------------
# LAYER 4: Dual Mass-Bounded Composite Output Constraint
# -------------------------------------------------------------
l4_bg = patches.FancyBboxPatch((3, 16.5), 94, 11.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                               facecolor=C_SLATE_BG, edgecolor=C_SLATE_BD, linewidth=1.8, zorder=2)
ax.add_patch(l4_bg)

t4_box = patches.FancyBboxPatch((5, 24.2), 90, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                facecolor=C_SLATE_BD, edgecolor='none', zorder=3)
ax.add_patch(t4_box)
ax.text(50, 25.45, 'LAYER 4: DUAL MASS-BOUNDED COMPOSITE OUTPUT OPERATOR', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)

# Highlighted Formula Callout Banner inside Layer 4
f4_banner = patches.FancyBboxPatch((5, 17.5), 90, 5.8, boxstyle="round,pad=0.3,rounding_size=0.6",
                                   facecolor=C_SLATE_CARD, edgecolor=C_SLATE_BD, linewidth=1.2, zorder=3)
ax.add_patch(f4_banner)

ax.text(50, 21.6, r'Dual Physical Mass-Bounding Operator Formulation:', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#1E293B', zorder=4)
ax.text(50, 19.8, r'$\hat{Q}(t) = \min\left(P(t) + Q_{\mathrm{inflow}}(t) + API(t), \; \max\left(0, \; Q_{\mathrm{base}}(t) + \hat{\varepsilon}(t)\right)\right)$', ha='center', va='center', fontsize=8.8, color='#0F172A', zorder=4)
ax.text(50, 18.2, r'✓ Prevents Unphysical Mass Creation and Conditional Mean Shrinkage During Out-of-Distribution Monsoon Shocks', ha='center', va='center', fontsize=7.5, fontweight='bold', color='#BE123C', zorder=4)

# Connector Arrow: Layer 4 -> Layer 5
draw_arrow(ax, 50, 16.5, 50, 12.5, color='#334155', label=r"Mass-Bounded Streamflow Estimates $\hat{Q}(t)$", fontsize=7.8)

# -------------------------------------------------------------
# LAYER 5: Out-of-Distribution Validation & Decision Support
# -------------------------------------------------------------
l5_bg = patches.FancyBboxPatch((3, 1.0), 94, 11.5, boxstyle="round,pad=0.5,rounding_size=1.2",
                               facecolor=C_ROSE_BG, edgecolor=C_ROSE_BD, linewidth=1.8, zorder=2)
ax.add_patch(l5_bg)

t5_box = patches.FancyBboxPatch((5, 9.2), 90, 2.5, boxstyle="round,pad=0.2,rounding_size=0.5",
                                facecolor=C_ROSE_BD, edgecolor='none', zorder=3)
ax.add_patch(t5_box)
ax.text(50, 10.45, 'LAYER 5: VALIDATION & OPERATIONAL DECISION SUPPORT APPLICATIONS', ha='center', va='center', fontsize=9.5, fontweight='bold', color='#FFFFFF', zorder=4)

# Layer 5 Sub-cards (3 Columns)
sub5_1 = patches.FancyBboxPatch((5, 2.0), 28.5, 6.5, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_ROSE_CARD, edgecolor=C_ROSE_BD, linewidth=1.0, zorder=3)
sub5_2 = patches.FancyBboxPatch((35.75, 2.0), 28.5, 6.5, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_ROSE_CARD, edgecolor=C_ROSE_BD, linewidth=1.0, zorder=3)
sub5_3 = patches.FancyBboxPatch((66.5, 2.0), 28.5, 6.5, boxstyle="round,pad=0.3,rounding_size=0.6", facecolor=C_ROSE_CARD, edgecolor=C_ROSE_BD, linewidth=1.0, zorder=3)
ax.add_patch(sub5_1); ax.add_patch(sub5_2); ax.add_patch(sub5_3)

ax.text(19.25, 7.0, 'EXTREME HOLDOUT EVAL', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#BE123C', zorder=4)
ax.text(19.25, 4.4, r'• Zero-Shot 2022 Mega-Flood' + '\n' + r'• $+350\%$ Monsoon Rainfall Shock', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(50.0, 7.0, 'BOOTSTRAP UNCERTAINTY', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#BE123C', zorder=4)
ax.text(50.0, 4.4, r'• Moving Block Bootstrap ($N=1000$)' + '\n' + r'• $95\%$ Confidence Intervals', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

ax.text(80.75, 7.0, 'OPERATIONAL DECISION', ha='center', va='center', fontsize=8.2, fontweight='bold', color='#BE123C', zorder=4)
ax.text(80.75, 4.4, r'• Guddu, Sukkur & Kotri Allocations' + '\n' + r'• Manchar Lake Volumetric Control', ha='center', va='center', fontsize=7.8, color='#1E293B', zorder=4)

# Save Outputs
out_png1 = 'paper_latex/figures/Figure_Methodology_Hierarchical_Framework.png'
out_png2 = 'paper_results/figures/Figure_Methodology_Hierarchical_Framework.png'

plt.savefig(out_png1, dpi=300, bbox_inches='tight')
plt.savefig(out_png2, dpi=300, bbox_inches='tight')
plt.close()

print(f"[SUCCESS] Generated Nature/IEEE-Grade Architecture Diagram -> {out_png1}")
