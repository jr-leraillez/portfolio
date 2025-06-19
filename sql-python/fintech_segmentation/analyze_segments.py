# analyze_segments.py
import sqlite3
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

# Set up paths
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


def create_database():
    """Create and populate SQLite database"""
    conn = sqlite3.connect(DATA_DIR / 'fintech.db')
    try:
        df = pd.read_csv(DATA_DIR / 'customers.csv')
        df.to_sql('customers', conn, if_exists='replace', index=False)
        conn.commit()
        print("✅ Database ready at data/fintech.db")
        return conn
    except Exception as e:
        print(f"❌ Database error: {e}")
        conn.close()
        raise


def segment_customers(conn):
    """Run segmentation query"""
    query = """
            SELECT customer_id, \
                   age, \
                   income, \
                   account_age_days, \
                   avg_monthly_transactions, \
                   avg_transaction_amount, \
                   CASE \
                       WHEN income > 70000 AND avg_transaction_amount > 200 THEN 'High-Value' \
                       WHEN account_age_days < 90 THEN 'New' \
                       WHEN avg_monthly_transactions < 5 THEN 'Dormant' \
                       ELSE 'Standard' \
                       END AS segment
            FROM customers \
            """
    return pd.read_sql(query, conn)


def plot_segments(segments):
    """Generate visualizations"""
    # Plot 1: Segment distribution
    plt.figure(figsize=(10, 5))
    segments['segment'].value_counts().plot(
        kind='bar',
        color=['#635bff', '#00d4ff', '#ff6b6b', '#adb5bd'],
        edgecolor='black'
    )
    plt.title('Customer Segments Distribution', pad=20)
    plt.xlabel('Segment')
    plt.ylabel('Number of Customers')
    plt.savefig(OUTPUT_DIR / 'segment_distribution.png', dpi=300, bbox_inches='tight')

    # Plot 2: Income by segment
    plt.figure(figsize=(10, 5))
    segments.boxplot(
        column='income',
        by='segment',
        grid=False,
        patch_artist=True,
        boxprops={'facecolor': '#635bff', 'alpha': 0.7}
    )
    plt.title('Income Distribution by Segment', pad=20)
    plt.suptitle('')
    plt.savefig(OUTPUT_DIR / 'income_by_segment.png', dpi=300, bbox_inches='tight')
    plt.close('all')


if __name__ == "__main__":
    try:
        # 1. Create and populate database
        conn = create_database()

        # 2. Run segmentation
        segments = segment_customers(conn)
        print("\nSample segments:")
        print(segments.head())

        # 3. Generate plots
        plot_segments(segments)
        print("\n✅ Visualizations saved to outputs/")

    finally:
        if 'conn' in locals():
            conn.close()
