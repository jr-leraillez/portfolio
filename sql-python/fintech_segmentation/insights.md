# Segmentation Insights

## Key Findings
1. **High-Value Customers (12%)**  
   - *Characteristics*: Income > £70k, large transactions  
   - *Strategy*: Offer premium services (e.g., wealth management)

2. **Dormant Customers (18%)**  
   - *Characteristics*: <5 transactions/month  
   - *Strategy*: Reactivation campaigns with fee waivers

## SQL Logic Highlight
```sql
CASE 
    WHEN income > 70000 AND avg_transaction_amount > 200 THEN 'High-Value'
    WHEN account_age_days < 90 THEN 'New'
    WHEN avg_monthly_transactions < 5 THEN 'Dormant'
    ELSE 'Standard'
END AS segment