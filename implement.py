import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# --------------------------------------------
# Objective 1: Exploratory data analysis


#Load the dataset
df = pd.read_excel(r"C:\Users\WIN11\Downloads\project python\Proj_data.xlsx")


# Basic structure and types
# print("Dataset Info:")
# print(df.info())

# # Summary statistics for all numerical columns
# print("\nSummary Statistics:")
# print(df.describe())

# #Convert TotalCharges to numeric and handle missing data
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
df_clean = df.dropna(subset=['TotalCharges']).copy()
df_clean['tenure'] = pd.to_numeric(df_clean['tenure'], errors='coerce')
df_clean['MonthlyCharges'] = pd.to_numeric(df_clean['MonthlyCharges'], errors='coerce')

# # # Check for missing values
# total_missing = df_clean.isnull().sum().sum()
# print(f"Total Missing Values in Cleaned Dataset: {total_missing}")


# # --------------------------------------------
# # Objective 2: Tenure and Revenue Analysis

# #Correlation between tenure and total charges
# tenure_totalcharges_corr = df_clean[['tenure', 'TotalCharges']].corr().iloc[0,1]
# print(f"Correlation between tenure and TotalCharges: {tenure_totalcharges_corr:.2f}")

# # Summary statistics for tenure
# tenure_stats = df_clean['tenure'].describe()
# print("Tenure Summary Statistics:")
# print(tenure_stats)

# # Scatter plot with regression line
# plt.figure(figsize=(8, 6))
# sns.regplot(x='tenure', y='TotalCharges', data=df_clean, scatter_kws={'alpha':0.5})   #alpha for transparency
# plt.title('Relationship between Tenure and TotalCharges')
# plt.xlabel('Tenure (months)')
# plt.ylabel('Total Charges')
# plt.show()

# # Boxplot for Outlier Detection in TotalCharges
# plt.figure(figsize=(8, 4))
# sns.boxplot(x=df_clean['TotalCharges'])
# plt.title('Outlier Detection in Total Charges')
# plt.show()

# # # Detecting Outliers in TotalCharges
# q1 = df_clean['TotalCharges'].quantile(0.25)
# q3 = df_clean['TotalCharges'].quantile(0.75)
# iqr = q3 - q1
# outliers_totalcharges = df_clean[(df_clean['TotalCharges'] < q1 - 1.5 * iqr) | (df_clean['TotalCharges'] > q3 + 1.5 * iqr)]
# print(f"TotalCharges Outliers: {len(outliers_totalcharges)} rows detected")

# # # --------------------------------------------
# # # Objective 3: Service Adoption and Bundling Opportunities

# services = ['OnlineSecurity', 'OnlineBackup', 'TechSupport', 'StreamingTV', 'StreamingMovies']
# adoption_rates = {}
# for service in services:
#     counts = df_clean[service].value_counts(normalize=True) * 100
#     adoption_rates[service] = counts.get("Yes", 0)

# print("Service Adoption Rates (in %):")
# print(adoption_rates)

# plt.figure(figsize=(8, 6))
# sns.barplot(x=list(adoption_rates.keys()), y=list(adoption_rates.values()))
# plt.title('Adoption Rates of Additional Services')
# plt.xlabel('Service')
# plt.ylabel('Adoption Rate (%)')
# plt.ylim(0, 100)
# plt.tight_layout()
# plt.show()

# # # --------------------------------------------
# # # Objective 4: Payment Method Preferences and Billing Differences

# payment_counts = df_clean['PaymentMethod'].value_counts()
# print("Payment Method Frequencies:")
# print(payment_counts)

# plt.figure(figsize=(8, 6))
# sns.barplot(x=payment_counts.index, y=payment_counts.values, palette="viridis")
# plt.title('Payment Method Distribution')
# plt.xlabel('Payment Method')
# plt.ylabel('Number of Customers')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# # # ANOVA test for MonthlyCharges across Payment Methods
# anova_result = stats.f_oneway(*[group['MonthlyCharges'].dropna().values for name, group in df_clean.groupby('PaymentMethod')])
# print("ANOVA test on MonthlyCharges by PaymentMethod:")
# print(f"F-statistic: {anova_result.statistic:.2f}, p-value: {anova_result.pvalue:.4f}")

# # # Boxplot to visualize outliers in MonthlyCharges across Payment Methods
# plt.figure(figsize=(10, 6))
# sns.boxplot(x='PaymentMethod', y='MonthlyCharges', data=df_clean)
# plt.title('Outlier Detection: Monthly Charges by Payment Method')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()

# # # Detecting Outliers in MonthlyCharges
# q1_m = df_clean['MonthlyCharges'].quantile(0.25)
# q3_m = df_clean['MonthlyCharges'].quantile(0.75)
# iqr_m = q3_m - q1_m
# outliers_monthlycharges = df_clean[(df_clean['MonthlyCharges'] < q1_m - 1.5 * iqr_m) | (df_clean['MonthlyCharges'] > q3_m + 1.5 * iqr_m)]
# print(f"MonthlyCharges Outliers: {len(outliers_monthlycharges)} rows detected")

# # # --------------------------------------------
# # # Objective 5: Statistical Test - Payment Method Comparison

group1 = df_clean[df_clean['PaymentMethod'] == 'Electronic check']['MonthlyCharges'].dropna()
group2 = df_clean[df_clean['PaymentMethod'] == 'Bank transfer (automatic)']['MonthlyCharges'].dropna()

t_stat, p_val = stats.ttest_ind(group1, group2, equal_var=False)
print("T-test comparing MonthlyCharges between 'Electronic check' and 'Bank transfer (automatic'):")
print(f"t-statistic: {t_stat:.2f}, p-value: {p_val:.4f}")
# # --------------------------------------------
# objective 6 :Chi-Square test between Contract type and Churn status

contingency_table = pd.crosstab(df_clean['Contract'], df_clean['Churn'])
chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

print("\nChi-Square Test: Contract vs Churn")
print(f"Chi-square statistic = {chi2_stat:.2f}, p-value = {p_val:.4f}, degrees of freedom = {dof}")
# # --------------------------------------------
# objective 7 :Z test :Is mean MonthlyCharges significantly different from $70?

from statsmodels.stats.weightstats import ztest
z_stat, p_val = ztest(df_clean['MonthlyCharges'].dropna(), value=70)
print("\nZ-Test: MonthlyCharges vs Hypothetical Mean = $70")
print(f"z-statistic = {z_stat:.2f}, p-value = {p_val:.4f}")

# # --------------------------------------------
# # Summary:
# # --------------------------------------------
# # Insight 1: Higher tenure is associated with higher total revenue.
# # Insight 2: Varying adoption rates suggest bundling opportunities.
# # Insight 3: Payment method usage varies significantly.
# # Insight 4: Statistical tests indicate real billing differences by method.
# # Insight 5: Outliers present in charges should be monitored for anomalies or special attention.
# # Insight 6: To determine whether there is a significant relationship between customer churn and contract type.
# # Insight 7:  To test whether the average monthly charges of customers significantly differ from a target or expected value (e.g., $70).

