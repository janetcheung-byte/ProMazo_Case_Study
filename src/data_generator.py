import pandas as pd
import numpy as np

# Define synthetic data
data = {
    "Portfolio": ["Global Cosmetics"] * 6 + ["Hair/Body"] * 4,
    "Geography": ["North America", "North America", "North America", "Europe", "Asia", "Asia",
                  "North America", "North America", "Europe", "South America"],
    "Category": ["Makeup"] * 3 + ["Makeup"] + ["Fragrance"] * 2 + ["Hair"] * 4,
    "Brand": ["BobbiBrown_NA"] * 3 + ["BobbiBrown_EU"] + ["Kilian_Asia"] * 2 + ["Aveda_NA"] * 2 + ["Aveda_EU", "ElizArden_SA"],
    "Segment": ["Lipstick_NA", "Mascara_NA", "Bronzer_NA", "Lipstick_EU", "Perfume_Asia", "BodyWash_Asia",
                "Shampoo_NA", "Conditioner_NA", "HairDye_EU", "HairDye_SA"],
    "Initial Sales": [2500000, 1500000, 800000, 2000000, 3000000, 1000000, 2200000, 1800000, 1500000, 1000000],
    "Margin (%)": [18, 15, 20, 18, 25, 22, 12, 13, 20, 18],
    "Trend (%)": [5, 2, 3, 6, 10, 4, 1, 2, 3, -2],
    "Contribution (%)": [30, 25, 15, 30, 40, 20, 30, 25, 20, 15],
    "Min Trend (%)": [2, 9, 3, 4, 5, 5, 8, 5, 3, 6],
    "Max Trend (%)": [20, 18, 20, 22, 25, 20, 15, 20, 15, 12],
    "Min Contribution (%)": [22.5, 18.75, 11.25, 22.5, 30.0, 15.0, 22.5, 18.75, 15.0, 11.25],
    "Max Contribution (%)": [100.0] * 10,
}

# Convert to DataFrame
df_synthetic = pd.DataFrame(data)

# Calculate lowSales and highSales based on trend ranges
df_synthetic["lowSales"] = df_synthetic["Initial Sales"] * (1 + df_synthetic["Min Trend (%)"] / 100)
df_synthetic["highSales"] = df_synthetic["Initial Sales"] * (1 + df_synthetic["Max Trend (%)"] / 100)

# Save the synthetic dataset to a CSV file
file_path = "synthetic_data_generated.csv"
df_synthetic.to_csv(file_path, index=False)

