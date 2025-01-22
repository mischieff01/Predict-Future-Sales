# 🌟 Predict Future Sales Flask App 🌟

Welcome to the **Predict Future Sales** web application! This interactive and visually appealing Flask-based app uses machine learning to deliver precise sales predictions for shops and items based on historical data. Designed with usability and performance in mind, this tool helps businesses make informed decisions with ease.

---

## ✨ Features

### 🚀 **Interactive User Interface**
- Dropdown menus for easy selection of shop and item IDs.
- Real-time display of predictions after submission.
- Fully responsive and mobile-friendly design.

### 📊 **Data-Driven Insights**
- Predict future sales by analyzing historical trends.
- Powered by a robust XGBoost model trained on a rich dataset.

### 🔗 **API-Driven Functionality**
- Dynamic endpoints for fetching available shop and item IDs.
- RESTful API integration for seamless data exchange.

---

## 📋 Prerequisites

Ensure you have the following before getting started:

- **Python Environment**: Python 3.7 or higher.
- **Libraries**: Flask, pandas, numpy, scikit-learn, xgboost, joblib.
- **Data and Model**:
  - Datasets: `sales_train.csv`, `items.csv`, `item_categories.csv`, `shops.csv`.
  - Pre-trained model: `sales_model.pkl`.

---

## 📂 File Structure

- **`app.py`**: The main Flask application file containing all logic and routes.
- **`templates/index.html`**: Interactive HTML template for the user interface.
- **Static Files**: Add custom styles and scripts for enhanced visual appeal.
- **Datasets and Model Files**: Necessary for accurate predictions.

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/mischieff01/Predict-Future-Sales.git
   cd Predict-Future-Sales
   ```

2. **Install Required Libraries**
   Use pip to install dependencies:
   ```bash
   pip install flask pandas numpy scikit-learn xgboost joblib
   ```

3. **Prepare Data and Model**
   - Place the dataset files (`sales_train.csv`, `items.csv`, `item_categories.csv`, `shops.csv`) in the specified directory.
   - Ensure the pre-trained model file (`sales_model.pkl`) is accessible as defined in `app.py`.

4. **Run the Application**
   Start the Flask server:
   ```bash
   python app.py
   ```
   Access the app at `http://127.0.0.1:5000/`.

5. **Enhance with Custom Features**
   - Personalize the frontend (`index.html`) with branding and animations.
   - Add advanced error handling and logging for better reliability.

---

## 🌟 How to Use the App

### Step 1: Launch the App
Open your browser and navigate to `http://127.0.0.1:5000/`.

### Step 2: Select Parameters
- **Shop ID**: Pick a shop ID from the dropdown menu.
- **Item ID**: Select an item ID from the dropdown menu.

### Step 3: Predict Sales
- Click the **"Predict"** button.
- Instantly view the predicted sales for your selection.

---

## 🖥️ API Endpoints

### `/predict`
- **Method**: POST
- **Purpose**: Predict sales for a given shop and item ID.
- **Input**:
  ```json
  {
      "shop_id": "<shop_id>",
      "item_id": "<item_id>"
  }
  ```
- **Output**:
  ```json
  {
      "prediction": <predicted_sales>
  }
  ```

### `/get_shop_ids`
- **Method**: GET
- **Purpose**: Fetch a list of available shop IDs.
- **Output**:
  ```json
  [<shop_id_1>, <shop_id_2>, ...]
  ```

### `/get_item_ids`
- **Method**: GET
- **Purpose**: Fetch a list of available item IDs.
- **Output**:
  ```json
  [<item_id_1>, <item_id_2>, ...]
  ```

---

## 🎨 Enhancements for Interactive Experience

- **Dynamic Dropdowns**: Populate shop and item IDs via API calls.
- **Instant Feedback**: See predictions immediately after submission.
- **Enhanced Visuals**: Add animations and tooltips for better engagement.

---

## 🔮 Future Improvements

- **Batch Predictions**: Support CSV uploads for bulk predictions.
- **Data Visualization**: Integrate charts to display trends and insights.
- **Model Training**: Include functionality to retrain the model with new data.

---

## 🙌 Acknowledgments

This project extends the [Predict-Future-Sales](https://github.com/mischieff01/Predict-Future-Sales.git) repository. Heartfelt thanks to the contributors for providing a strong foundation for this application.

---

## 📜 License

This project is licensed under the MIT License. Check the original repository for detailed licensing information.

---

## 🚀 Get Started Today!

🎉 Dive into the **Predict Future Sales** app and revolutionize your business decisions. Feedback and contributions are always welcome! 🌟