# **ProMazo Case Study**
**Author:** Janet C
**Date:** 02/24/2025  

---

##  **Introduction**
This project is a **data-driven forecasting and optimization solution** for Acme’s sales prediction model. The algorithm is designed to predict **future sales and margins** while adhering to **trend growth and contribution constraints** across different organizational levels.

The solution addresses the following objectives:  
✅ **Maximize Sales**  
✅ **Maximize Margin**  
✅ **Hit a Sales Target While Maximizing Margin**  
✅ **Hit a Margin Target While Maximizing Sales**  
✅ **Generate 5-Year Projections**  

---

## **📂 Project Structure**
```bash
📁 ProMazo_Case_Study
│── 📜 README.md              # Project documentation
│── 📊 synthetic_data.csv      # Generated dataset with realistic sales & margin data
│── 📊 5_year_projections.csv  # Model's output with 5-year projections
│── 📂 src/                    # Source code directory
│    ├── 📜 data_preprocessing.py  # Script to generate synthetic data
│    ├── 📜 sales_maximization.py   # Algorithm for maximizing sales
│    ├── 📜 margin_maximization.py  # Algorithm for maximizing margin
│    ├── 📜 margin_maximization_sales_target.py  # Hit A Sales Target While Maximizing Margin
│    ├── 📜 margin_maximization_margin_target.py  # Hit A Margin Target While Maximizing Sales:
│    ├── 📜 projections.py          # 5-year projections      
```


---

## **🔹 Dataset Details**
The synthetic dataset follows Acme’s **hierarchical structure**:
- **Portfolio → Geography → Category → Brand → Segment**
- Each **segment** contains:
  - **Initial Sales**
  - **Margin (%)**
  - **Trend (%)**
  - **Contribution (%)**  
  - **Growth Constraints (Min/Max Trend & Contribution)**  

---

## **📊 Methodology**
### **1️⃣ Synthetic Data Generation**
- Used **Pandas & NumPy** to create realistic sales data.
- Ensured **segment contributions sum to 100% per brand**.

### **2️⃣ Optimization Models**
Each objective was solved using **Linear Programming (LP) with PuLP**:

#### **✅ Maximize Sales**
- **Objective:** Maximize total sales while respecting **trend & contribution constraints**.
- **Solution:** Used **LP Solver** to optimize revenue growth.

#### **✅ Maximize Margin**
- **Objective:** Maximize total profit margin within given sales constraints.
- **Solution:** LP solver adjusted **sales allocation for highest profitability**.

#### **✅ Hit a Sales Target While Maximizing Margin**
- **Objective:** Achieve a fixed sales target **while ensuring maximum profitability**.
- **Solution:** Introduced a **minimum revenue constraint** while maximizing margin.

#### **✅ Hit a Margin Target While Maximizing Sales**
- **Objective:** Ensure a **minimum margin** while maximizing revenue growth.
- **Solution:** Constrained the **profit margin to be above a defined threshold**.

#### **✅ Generate 5-Year Projections**
- **Objective:** Predict sales growth over **5 years** while allowing annual adjustments.
- **Solution:** Used **dynamic constraints** to simulate realistic market changes.

---

## **📊 Results & Insights**
| Objective  | Key Findings |
|------------|-------------|
| **Maximize Sales**  | Found the highest possible revenue within constraints. |
| **Maximize Margin**  | Identified the most profitable segment allocation. |
| **Hit Sales Target** | Met the sales goal while **optimizing margins**. |
| **Hit Margin Target** | Ensured **profitability** while maximizing revenue. |
| **5-Year Projection** | Modeled future trends with **constraint adjustments**. |

✅ **Key Takeaways:**  
- **Sales vs. Profit Tradeoff:** High sales do not always mean high margins.  
- **Growth Constraints Impact Feasibility:** Strict constraints **limit possible outcomes**.  
- **Scenario Testing Improves Planning:** 5-year projections **help leadership decisions**.

---

## **🚀 Installation & Setup**
### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/[your-username]/ProMazo_Case_Study.git
cd ProMazo_Case_Study
