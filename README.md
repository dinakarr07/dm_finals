
# Stock Price Prediction using Linear Regression, LSTM, and ARIMA

This project focuses on predicting Microsoft (MSFT) stock prices using three different approaches:
- **Linear Regression** (for simplicity and interpretability)
- **LSTM Neural Networks** (for capturing complex temporal dependencies)
- **ARIMA** (a classical statistical method for time series forecasting)

It includes end-to-end implementation: data extraction, preparation, training, evaluation, forecasting, sentiment analysis, and visualization.

## Project Structure

```
├── api/                # Scripts to extract historical stock data from Polygon API
├── llm/                # LLM-based sentiment analysis using news data and OpenAI API
├── stocks_data.csv     # Main dataset for modeling
├── actual_jan.csv      # Actual January prices for model comparison
├── linear_regression_model.ipynb
├── lstm_model.ipynb
├── arima_model.ipynb
├── DataWrangling.ipynb.#filtered and extracted the features from the raw data which is collected from API
├── README.md
├── requirements.txt
```

## Features
- Predict next-day and multi-day stock prices
- Compare model accuracy using RMSE, MAPE
- Analyze stock market sentiment using news articles and LLMs
- Visualize actual vs predicted prices
- Extract insights and investor suggestions from LLM

##  Technologies Used
- Python (NumPy, Pandas, Matplotlib, Seaborn)
- Scikit-learn
- TensorFlow / Keras
- Statsmodels (ARIMA)
- NewsAPI
- OpenAI + LangChain
- Polygon.io API
- yFinance

## How to Run

1. Clone the repo and navigate to the project directory.
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run scripts:
   - `api/`: Extract stock data
   - `llm/`: Run sentiment analysis
   - `linear_regression_model.py`
   - `lstm_model.py`
   - `arima_model.py`

> Make sure `stocks_data.csv` and `actual_jan.csv` are available.

## Sample Output
- Model performance metrics
- Future forecast plots
- Sentiment trend visualizations
- LLM-generated investor reports


## Author
Dinakar Reddy DonthiReddy
