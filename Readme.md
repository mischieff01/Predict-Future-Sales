# Sales Analysis Project

This project is focused on analyzing sales data to extract meaningful insights and trends. The project includes data preprocessing, feature extraction, and visualization techniques to understand the sales patterns over time.

## Features of the Notebook

1. **Library Imports**:
   - Utilizes essential Python libraries such as `numpy`, `pandas`, `matplotlib`, and `seaborn` for data manipulation and visualization.
   - Includes `scikit-learn` for preprocessing and additional tools for advanced analysis.

2. **Data Loading**:
   - Loads datasets, including `sales_train.csv`, and other related files.
   - Uses `pandas` for efficient data handling.

3. **Data Cleaning**:
   - Handles missing values with `isnull().sum()`.
   - Processes and formats columns like `date` into datetime format for better analysis.

4. **Feature Engineering**:
   - Extracts `year` and `month` from the `date` column to allow temporal analysis.
   - Groups data by `date_block_num` for aggregated insights.

5. **Visualization**:
   - Utilizes `matplotlib` to visualize monthly sales trends over different years.
   - Implements custom plot settings for enhanced readability, such as `MONTHS`, `LINEWIDTH`, and `ALPHA` parameters.

## Key Functions and Code Snippets

### Extract Year and Month:
```python
# Convert date column to datetime
sales['date'] = pd.to_datetime(sales['date'], format='%d.%m.%Y')
sales['year'] = sales['date'].dt.year
sales['month'] = sales['date'].dt.month
```

### Check for Missing Values:
```python
# Check for null values
print(sales.isnull().sum())
```

### Group by Date Block:
```python
df = sales.groupby('date_block_num', as_index=False).agg({
    'year': 'first',
    'month': 'first',
    'item_cnt_day': 'sum'
})
```

### Plot Sales for a Specific Year:
```python
plt.figure(figsize=(10, 6))
plt.plot(MONTHS, df[df['year'] == 2013].item_cnt_month, '-o', color='steelblue', linewidth=LINEWIDTH, alpha=ALPHA, label='2013')
plt.show()
```

## Troubleshooting

### Common Errors:
- **`KeyError: 'year'`**:
  - Cause: The `year` column might not exist in the DataFrame.
  - Fix: Ensure the `year` column is created during preprocessing.
  ```python
  sales['year'] = sales['date'].dt.year
  ```

### Verifying Data:
- Check the columns in the DataFrame:
  ```python
  print(df.columns)
  ```
- Ensure `date` column is correctly converted:
  ```python
  sales['date'] = pd.to_datetime(sales['date'], format='%d.%m.%Y')
  ```

## Dependencies
- Python 3.x
- Libraries:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sales-analysis.git
   cd sales-analysis
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Open the Jupyter Notebook:
   ```bash
   jupyter notebook sales_analysis.ipynb
   ```

4. Run the cells sequentially to process and analyze the sales data.

## How to Use This Repository
1. **Understand the Structure**:
   - The repository contains the main notebook (`sales_analysis.ipynb`), datasets (`data/` folder), and a requirements file (`requirements.txt`).

2. **Prepare the Data**:
   - Place the datasets (e.g., `sales_train.csv`) in the `data/` folder.

3. **Run the Analysis**:
   - Follow the notebook to preprocess, clean, and analyze the sales data.

4. **Extend the Project**:
   - Modify the notebook to include additional features, visualizations, or analyses as needed.

## Output
- Monthly and yearly sales trends.
- Insights into data patterns and seasonality.

## Future Work
- Incorporate machine learning models for sales prediction.
- Add interactive visualizations using tools like Plotly or Dash.
- Enhance data preprocessing with automated anomaly detection.

