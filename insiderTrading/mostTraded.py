import pandas as pd

# Load the CSV file
# Replace 'path_to_your_csv.csv' with the actual path to your CSV file
df = pd.read_csv('trading.csv')

# Ensure consistency in transaction types (e.g., all to uppercase)
df['Transaction Type'] = df['Transaction'].str.upper()

# Group by 'Symbol' and 'Transaction Type', then count occurrences
transaction_counts = df.groupby(['Symbol', 'Transaction Type']).size().reset_index(name='Count')

# Sort the transactions to find the most bought and sold stocks
most_traded_symbols = transaction_counts.sort_values(by='Count', ascending=False)

# Find the most bought stocks
most_bought_symbols = most_traded_symbols[most_traded_symbols['Transaction Type'] == 'BUY'].head()

# Find the most sold stocks
most_sold_symbols = most_traded_symbols[most_traded_symbols['Transaction Type'] == 'SELL'].head()

# Display the results
print("Most Bought Stocks:")
print(most_bought_symbols)

print("\nMost Sold Stocks:")
print(most_sold_symbols)
