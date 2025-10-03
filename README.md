# Easy Trade – Demo Trading Simulator

A web-based stock trading simulator built with Flask and PostgreSQL, designed to provide a realistic trading experience without financial risk. Users can search stocks, view live prices via Yahoo Finance, manage a simulated portfolio, and generate PDF reports of trades and account history.

---

## Features
- Secure user authentication (sign-up, login, password management with bcrypt)
- Live stock data via Yahoo Finance (yfinance)
- Portfolio management: cash balance, holdings, and total value
- Trading simulator: buy/sell stocks with validation on trade size and available funds
- Account history: view deposits and withdrawals
- Trade history: browse and filter by date range
- Generate downloadable PDF reports (reportlab)
- Clean Bootstrap UI with custom theming

---

## Tech Stack
- Backend: Flask (Python 3.13)
- Database: PostgreSQL (psycopg2)
- Frontend: HTML, Bootstrap 5, Jinja2 templates
- Libraries: yfinance, reportlab, bcrypt, pandas, python-dotenv

---

## Installation

### Prerequisites
- Python 3.11+ (tested on Python 3.13)
- PostgreSQL installed and running
- Git (optional)

### Clone the repository
git clone https://github.com/alexander-kireev/demo_trading_app.git
cd demo_trading_app

### Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

### Install dependencies
pip install -r requirements.txt

---

## Configuration

You must set up a PostgreSQL database manually:

1. Create a PostgreSQL user and database:

   ```sql
   CREATE USER trading_user WITH PASSWORD 'yourpassword';
   CREATE DATABASE trading_app OWNER trading_user;


2. Create a `.env` file in the project root:
   DATABASE_URL=postgresql://trading_user:yourpassword@localhost:5432/trading_app
   SECRET_KEY=your_secret_key_here

---

## Running the App
Start the Flask development server:
flask run

Visit:
http://127.0.0.1:5000/

---

## Requirements
The app depends on the following packages (pinned to tested versions):

Flask==3.1.2
bcrypt==4.3.0
reportlab==4.4.4
python-dotenv==1.1.1
pandas==2.3.2
psycopg2==2.9.10
yfinance==0.2.66

Install them with:
pip install -r requirements.txt

---

## Future Improvements
- Portfolio performance charts
- Expanded trade analytics (PnL, ratios)
- Leaderboards for multiple users
- Docker support for easier setup
- Deployment to cloud (Heroku, Render, Fly.io)

---

## License
This project is for educational/demo purposes only and is not intended for real financial trading.

---

## Author
Developed by Alexander Kireev (2025).
