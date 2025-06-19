# generate_data.py
import pandas as pd
import numpy as np

def generate_customer_data():
    np.random.seed(42)  # For reproducible results
    data = {
        'customer_id': range(1, 501),
        'age': np.random.randint(18, 70, 500),
        'income': np.abs(np.random.normal(50000, 15000, 500)).astype(int),
        'account_age_days': np.random.randint(30, 365*3, 500),
        'avg_monthly_transactions': np.random.poisson(15, 500),
        'avg_transaction_amount': np.abs(np.random.normal(150, 50, 500)).astype(int),
        'region': np.random.choice(['London', 'Manchester', 'Birmingham', 'Leeds', 'Bristol'], 500)
    }
    df = pd.DataFrame(data)
    df.to_csv('data/customers.csv', index=False)
    print("✅ Generated data/customers.csv")

if __name__ == "__main__":
    generate_customer_data()