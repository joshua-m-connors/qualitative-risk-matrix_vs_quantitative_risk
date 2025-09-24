import random
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- Classification Functions ---

def classify_likelihood(value):
    if 0.01 <= value <= 0.2:
        return 'Very Low'
    elif 0.21 <= value <= 0.4:
        return 'Low'
    elif 0.41 <= value <= 0.6:
        return 'Medium'
    elif 0.61 <= value <= 0.8:
        return 'High'
    elif 0.81 <= value <= 1.0:
        return 'Very High'
    else:
        return 'Negligible'

def classify_impact(value):
    if 100000 <= value <= 1000000:
        return 'Very Low'
    elif 1000001 <= value <= 2500000:
        return 'Low'
    elif 2500001 <= value <= 5000000:
        return 'Medium'
    elif 5000001 <= value <= 10000000:
        return 'High'
    else:
        return 'Very High'

def classify_risk(value):
    if 1 <= value <= 500000:
        return 'Very Low'
    elif 500001 <= value <= 1000000:
        return 'Low'
    elif 1000001 <= value <= 2500000:
        return 'Medium'
    elif 2500001 <= value <= 5000000:
        return 'High'
    else:
        return 'Very High'

# --- Generate Risks ---

risks = []

for _ in range(5000):
    likelihood = round(random.uniform(0, 1), 4)
    impact = round(random.uniform(100000, 20000000), 2)
    risk_score = round(likelihood * impact, 2)

    likelihood_level = classify_likelihood(likelihood)
    impact_level = classify_impact(impact)
    risk_level = classify_risk(risk_score)

    risks.append({
        'Likelihood': likelihood,
        'Impact': impact,
        'Risk Score': risk_score,
        'Likelihood Level': likelihood_level,
        'Impact Level': impact_level,
        'Risk Level': risk_level
    })

df = pd.DataFrame(risks)

# --- Map Levels to Matrix Coordinates ---

level_order = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
level_to_num = {level: i for i, level in enumerate(level_order)}

df['Likelihood Num'] = df['Likelihood Level'].map(level_to_num)
df['Impact Num'] = df['Impact Level'].map(level_to_num)

# --- Add jitter for visual separation ---
jitter_strength = 0.45
df['Impact Jitter'] = df['Impact Num'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(df))
df['Likelihood Jitter'] = df['Likelihood Num'] + np.random.uniform(-jitter_strength, jitter_strength, size=len(df))

# --- Plotting ---

# Define color palette
risk_palette = {
    'Very Low': '#008000',
    'Low': '#ADFF2F',
    'Medium': '#FFFF00',
    'High': '#FFA500',
    'Very High': '#8B0000'
}

# --- Create Quintiles ---
df['Risk Quintile'] = pd.qcut(df['Risk Score'], 5, labels=False)

# Map each risk level to base color (same as before)
df['Base Color'] = df['Risk Level'].map(risk_palette)

# Map quintiles to alpha values (0.3 for lowest, 0.7 for highest)
quintile_to_alpha = {
    0: 0.3,
    1: 0.45,
    2: 0.55,
    3: 0.65,
    4: 0.75
}
df['Alpha'] = df['Risk Quintile'].map(quintile_to_alpha)

# --- Plotting ---
plt.figure(figsize=(10, 8))
sns.set(style="whitegrid")

# Plot each point manually to use individual alpha levels
for _, row in df.iterrows():
    plt.scatter(
        row['Impact Jitter'],
        row['Likelihood Jitter'],
        color=row['Base Color'],
        alpha=row['Alpha'],
        edgecolor='black',
        linewidth=0.2,
        s=60
    )

# Format plot
plt.xticks(ticks=range(5), labels=level_order, rotation=45)
plt.yticks(ticks=range(5), labels=level_order)
plt.xlabel('Impact Level')
plt.ylabel('Likelihood Level')
plt.title('Risk Matrix (5x5) with Risk Level Coloring and Risk Score Quintile Shading')
plt.grid(True)
plt.tight_layout()

# Legend (same as original)
risk_legend_handles = [
    plt.Line2D([0], [0], marker='o', color='w',
               label=level,
               markerfacecolor=color,
               markersize=10,
               markeredgecolor='black')
    for level, color in risk_palette.items()
]
plt.legend(handles=risk_legend_handles, title='Risk Level', loc='upper left', bbox_to_anchor=(1, 1))

# Show plot
plt.show()
