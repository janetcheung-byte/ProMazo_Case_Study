# Modify the optimization script to fix the unbounded issue by adding constraints

import pulp

# Load the original dataset before optimization
file_path_original = "synthetic_data.csv"
df_original = pd.read_csv(file_path_original)

# Define the number of years for projection
NUM_YEARS = 5

# Create the LP problem for multi-year projection with a modified objective
model_5yr_fixed = pulp.LpProblem("5YearProjection_MaximizeSales", pulp.LpMaximize)

# Dictionary to store decision variables for each year and segment
sales_vars = {year: {} for year in range(1, NUM_YEARS + 1)}

# Create decision variables for each segment and year, ensuring Year 1 starts at Initial Sales
for year in range(1, NUM_YEARS + 1):
    for idx, row in df_original.iterrows():
        var = pulp.LpVariable(
            f"Sales_{idx}_Year{year}", 
            lowBound=row["Initial Sales"] if year == 1 else 0, 
            upBound=row["highSales"],  # Adding upper bound to prevent unbounded solutions
            cat=pulp.LpContinuous
        )
        sales_vars[year][idx] = var

# Objective: Maximize total revenue while ensuring a minimum margin
model_5yr_fixed += pulp.lpSum(
    sales_vars[year][idx] for year in range(1, NUM_YEARS + 1) for idx, row in df_original.iterrows()
), "Total_5Year_Revenue"

# Apply yearly trend constraints (making them slightly tighter)
for year in range(2, NUM_YEARS + 1):  # Start from year 2
    for idx, row in df_original.iterrows():
        min_trend = row["Min Trend (%)"] / 100.0
        max_trend = row["Max Trend (%)"] / 100.0

        model_5yr_fixed += (
            sales_vars[year][idx] >= (0.85 + min_trend) * sales_vars[year - 1][idx],
            f"Tighter_MinTrend_{idx}_Year{year}"
        )

        model_5yr_fixed += (
            sales_vars[year][idx] <= (1.15 + max_trend) * sales_vars[year - 1][idx],
            f"Tighter_MaxTrend_{idx}_Year{year}"
        )

# Add a total sales limit per year to prevent infinite growth
max_total_sales = 1.5 * df_original["Initial Sales"].sum()  # 1.5x total initial sales
for year in range(1, NUM_YEARS + 1):
    model_5yr_fixed += (
        pulp.lpSum(sales_vars[year].values()) <= max_total_sales,
        f"Total_Sales_Limit_Year{year}"
    )

# Solve the Model with Debugging Mode Enabled
solution_status_5yr_fixed = model_5yr_fixed.solve(pulp.PULP_CBC_CMD(msg=True))

# Output solution status
solution_status = pulp.LpStatus[solution_status_5yr_fixed]
print("Solution Status:", solution_status)

# Check if an optimal solution was found
if solution_status == "Optimal":
    total_sales_5yr_fixed = pulp.value(model_5yr_fixed.objective)
    print(f"\nMaximum Achievable Revenue Over 5 Years: ${total_sales_5yr_fixed:,.2f}\n")

    # Collect results into a dataframe
    results_fixed = []
    for year in range(1, NUM_YEARS + 1):
        for idx, row in df_original.iterrows():
            sales_value = pulp.value(sales_vars[year][idx])
            results_fixed.append([year, row["Portfolio"], row["Geography"], row["Category"], row["Brand"], row["Segment"], sales_value])

    # Convert results into DataFrame
    df_results_fixed = pd.DataFrame(results_fixed, columns=["Year", "Portfolio", "Geography", "Category", "Brand", "Segment", "Optimized Sales"])

    # Save the optimized results to a CSV file
    fixed_output_path = "5_year_projections.csv"
    df_results_fixed.to_csv(fixed_output_path, index=False)
    print("Optimized 5-Year Projections saved to:", fixed_output_path)

else:
    print("No optimal solution found. Investigating further constraints.")
