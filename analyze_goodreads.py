import pandas as pd
import sqlite3
from tabulate import tabulate

# Load CSV into Pandas
book_data = pd.read_csv("grca_nominees2024.csv")
books_rating = pd.read_csv("rating.csv")

# Create an in-memory SQLite database
conn = sqlite3.connect(":memory:")

# Store DataFrame into SQL table
book_data.to_sql("books", conn, if_exists="replace", index=False)
books_rating.to_sql("rating", conn, if_exists="replace", index=False)

# SQL Query //  Query see the books in the romance category that have more than 4 stars rating average.
df = pd.read_sql_query(
    """
    SELECT title, AVG(rating) AS 'Average Rating'
    FROM rating
    WHERE title IN (SELECT title FROM books WHERE [Nomination Category] = 'Romance')
    GROUP BY title
    HAVING AVG(rating) > 4
    """,
    conn
)

# Format output using tabulate
table_output = tabulate(df, headers="keys", tablefmt="psql", showindex=False)

# Print in terminal
print(table_output)

# Save results to a text file
with open("all_queries_result.txt", "w", encoding="utf-8") as file:
    file.write(table_output)

conn.close()

print("All query results saved to 'all_queries_result.txt' in tabulated format! 🎉")
