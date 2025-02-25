import pandas as pd
import pulp

# Load the dataset (Make sure to adjust the file path if needed)
df = pd.read_csv("obj_1_test_with_corrected_contributions.csv")

# Create the LP problem for maximizing margin
model_margin = pulp.LpProblem("MaximizeMargin", pulp.LpMaximize)

# Decision variables for each segment: New Sales
new_sales_vars = {}
for idx, row in df.iterrows():
    init_sales = row["Initial Sales"]
    
    # Convert integer percentages to decimal form
    min_trend = row["Min Trend (%)"] / 100.0
    max_trend = row["Max Trend (%)"] / 100.0
    
    # Lower and upper bounds for new sales based on trend constraints
    low_bound = (1 + min_trend) * init_sales
    up_bound = (1 + max_trend) * init_sales
    
    # Create a continuous decision variable for the new sales of this segment
    var = pulp.LpVariable(
        f"NewSales_{idx}",
        lowBound=low_bound,
        upBound=up_bound,
        cat=pulp.LpContinuous
    )
    new_sales_vars[idx] = var

# Create a dictionary to track "Brand Totals"
brand_totals = {}
for brand in df["Brand"].unique():
    brand_totals[brand] = pulp.LpVariable(
        f"BrandTotal_{brand}",
        lowBound=0,
        cat=pulp.LpContinuous
    )

# Objective: Maximize Total Margin
model_margin += pulp.lpSum((row["Margin (%)"] / 100.0) * new_sales_vars[idx] for idx, row in df.iterrows()), "Total_Margin"

# Constraints
# BrandTotal = sum of NewSales for all segments of that Brand
for brand in df["Brand"].unique():
    brand_indices = df[df["Brand"] == brand].index
    model_margin += (
        brand_totals[brand] == pulp.lpSum([new_sales_vars[i] for i in brand_indices]),
        f"BrandTotal_{brand}_Constraint"
    )

# Contribution constraints
for idx, row in df.iterrows():
    brand = row["Brand"]
    min_contrib = row["Min Contribution (%)"] / 100.0
    max_contrib = row["Max Contribution (%)"] / 100.0
    
    model_margin += (
        new_sales_vars[idx] >= min_contrib * brand_totals[brand],
        f"MinContrib_{idx}"
    )
    
    model_margin += (
        new_sales_vars[idx] <= max_contrib * brand_totals[brand],
        f"MaxContrib_{idx}"
    )

# Solve the Model
solution_status_margin = model_margin.solve(pulp.PULP_CBC_CMD(msg=False))
print("Solution Status:", pulp.LpStatus[solution_status_margin])

if pulp.LpStatus[solution_status_margin] == "Optimal":
    total_margin = pulp.value(model_margin.objective)
    print(f"\nMaximum Achievable Total Margin: ${total_margin:,.2f}\n")

    # Append Results to df
    optimized_sales = []
    optimized_margins = []
    new_trend_vals = []
    new_contribution_vals = []
    
    for idx, row in df.iterrows():
        brand = row["Brand"]
        init_sales = row["Initial Sales"]
        margin_rate = row["Margin (%)"] / 100.0
        
        seg_sales_val = pulp.value(new_sales_vars[idx])
        optimized_sales.append(seg_sales_val)
        
        margin_value = seg_sales_val * margin_rate
        optimized_margins.append(margin_value)
        
        trend_percentage = ((seg_sales_val - init_sales) / init_sales) * 100
        new_trend_vals.append(trend_percentage)
        
        brand_total_val = pulp.value(brand_totals[brand])
        if brand_total_val > 0:
            contrib_percentage = (seg_sales_val / brand_total_val) * 100
        else:
            contrib_percentage = 0
        new_contribution_vals.append(contrib_percentage)
    
    # Add columns to df
    df["Optimized Sales"] = optimized_sales
    df["Optimized Margin"] = optimized_margins
    df["New Trend (%)"] = new_trend_vals
    df["New Contribution (%)"] = new_contribution_vals

    # Save the optimized results to a CSV file
    df.to_csv("obj_3_optimized_margin_results.csv", index=False)
    print("Optimized results saved to 'optimized_margin_results.csv'")
else:
    print("No optimal solution found.")
