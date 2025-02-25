# Define a target margin percentage (example: 20%)
target_margin = 20

# Filter data to include only units meeting or exceeding the target margin
df_margin_target = df[df['Margin (%)'] >= target_margin]

# Sort by Sales to maximize sales while meeting the margin target
df_margin_target_sorted = df_margin_target.sort_values(by='Initial Sales', ascending=False)

# Display the filtered and sorted dataframe
print(df_margin_target_sorted)
