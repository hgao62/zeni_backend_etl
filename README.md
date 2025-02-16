# Stock Data ETL Pipeline with Interactive Dashboard

## Project Overview
A comprehensive data engineering project that extracts, transforms, and loads stock market data, culminating in an interactive web-based dashboard for financial analysis.
![overview](/docs/architecture_diagram.png)

## 🚀 Key Features

### Data Pipeline
- Extract stock data from Yahoo Finance API
  - Real-time stock history
  - Financial information
  - Exchange rates
  - Company news

### Data Processing
- Advanced data transformation techniques
  - Normalize stock data
  - Calculate daily and cumulative returns
  - Compute moving averages
  - Standardize prices to USD
  - Sector-based analysis

### Interactive Dashboard
🔗 **Live Dashboard**: [View Stock Market Dashboard](https://public.tableau.com/app/profile/zheng.zhang3017/viz/stock_etl_dashboard/STOCKHISTORY)

#### Dashboard Highlights
- Comprehensive stock price tracking
- Multi-stock comparison
- Real-time performance metrics
- Sector distribution visualization
- Cumulative return analysis

#### Dashboard Visualizations
- Stock Price Over Time
- Trading Volume Analysis
- Sector Distribution
- Cumulative Returns
- Stock Summary Statistics

## 🛠 Technologies Used

### Backend
- Python
- SQLAlchemy
- Pandas
- Yfinance
- MySQL

### Data Processing
- Docker
- Apache Airflow

### Dashboard
- Tableau
- Web Hosting Platform

## 📊 Key Metrics Tracked
- Stock Prices
- Percentage Changes
- Trading Volumes
- Sector Allocations
- Cumulative Returns

## 🔧 Prerequisites
- Python 3.9+
- Docker
- Docker Compose
- Tableau (for dashboard development)

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/stock-etl-pipeline.git
cd stock-etl-pipeline
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run ETL Pipeline
```bash
python main.py
```

### 4. Launch with Docker
```bash
docker-compose up --build
```

## 🧪 Testing
- Pytest for unit testing
- Coverage of critical functions
- Static code analysis tools
  - Pylint
  - Mypy
  - Black
  - isort

## 📈 Dashboard Deployment
- Hosted on web platform
- Real-time data updates
- Responsive design
- Interactive filters and drill-down capabilities

## 🔜 Future Roadmap
- Machine learning price predictions
- Extended historical data analysis
- More advanced visualization techniques
- Real-time alerting system
