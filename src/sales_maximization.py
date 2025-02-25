import pulp
import pandas as pd

# For reference, df columns:
# ['Portfolio', 'Geography', 'Category', 'Brand', 'Segment',
#  'Initial Sales', 'Margin (%)', 'Trend (%)', 'Contribution (%)',
#  'Min Trend (%)', 'Max Trend (%)', 'Min Contribution (%)', 'Max Contribution (%)']

# Create the LP problem
model = pulp.LpProblem("MaximizeSales", pulp.LpMaximize)

# Decision variables for each row: NewSales_i
new_sales_vars = {}
for idx, row in df.iterrows():
    init_sales = row["Initial Sales"]
    
    # Convert integer percentages to decimal form
    min_trend = row["Min Trend (%)"] / 100.0
    max_trend = row["Max Trend (%)"] / 100.0
    
    # Lower and upper bounds for new sales based on trend constraints
    low_bound = (1 + min_trend) * init_sales
    up_bound  = (1 + max_trend) * init_sales
    
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

# -----------------------------
# 2. Objective: Maximize sum of all NewSales
# -----------------------------
model += pulp.lpSum(new_sales_vars.values()), "Total_New_Sales"

# -----------------------------
# 3. Constraints
# -----------------------------
# 3a) BrandTotal = sum of NewSales for all segments of that Brand
for brand in df["Brand"].unique():
    # Get indexes of rows for this brand
    brand_indices = df[df["Brand"] == brand].index
    model += (
        brand_totals[brand] == pulp.lpSum([new_sales_vars[i] for i in brand_indices]),
        f"BrandTotal_{brand}_Constraint"
    )

# 3b) Contribution constraints: 
#     min_contrib <= (NewSales_i / BrandTotal) <= max_contrib
#     => NewSales_i >= min_contrib * BrandTotal
#        NewSales_i <= max_contrib * BrandTotal
for idx, row in df.iterrows():
    brand = row["Brand"]
    min_contrib = row["Min Contribution (%)"] / 100.0
    max_contrib = row["Max Contribution (%)"] / 100.0
    
    # min_contrib * BrandTotal <= NewSales_i
    model += (
        new_sales_vars[idx] >= min_contrib * brand_totals[brand],
        f"MinContrib_{idx}"
    )
    # NewSales_i <= max_contrib * BrandTotal
    model += (
        new_sales_vars[idx] <= max_contrib * brand_totals[brand],
        f"MaxContrib_{idx}"
    )

# -----------------------------
# 4. Solve the Model
# -----------------------------
solution_status = model.solve(pulp.PULP_CBC_CMD(msg=False))
print("Solution Status:", pulp.LpStatus[solution_status])

if pulp.LpStatus[solution_status] == "Optimal":
    # Retrieve the optimized total sales
    total_sales = pulp.value(model.objective)
    print(f"\nMaximum Achievable Total Sales: ${total_sales:,.2f}\n")

    # -----------------------------
    # 5. Append Results to df
    # -----------------------------
    optimized_sales = []
    new_trend_vals = []
    new_contribution_vals = []
    
    for idx, row in df.iterrows():
        brand = row["Brand"]
        init_sales = row["Initial Sales"]
        
        # Optimized new sales for this segment
        seg_sales_val = pulp.value(new_sales_vars[idx])
        optimized_sales.append(seg_sales_val)
        
        # Compute new trend: ((NewSales - InitialSales) / InitialSales) * 100
        trend_percentage = ((seg_sales_val - init_sales) / init_sales) * 100
        new_trend_vals.append(trend_percentage)
        
        # Compute new contribution: (NewSales / BrandTotal) * 100
        brand_total_val = pulp.value(brand_totals[brand])
        if brand_total_val > 0:
            contrib_percentage = (seg_sales_val / brand_total_val) * 100
        else:
            contrib_percentage = 0
        new_contribution_vals.append(contrib_percentage)
    
    # Add columns to df
    df["Optimized Sales"] = optimized_sales
    df["New Trend (%)"]   = new_trend_vals
    df["New Contribution (%)"] = new_contribution_vals
    
    # -----------------------------
    # 6. Show the Final Data
    # -----------------------------
    print(df.to_string(index=False))
else:
    print("No optimal solution found.")
