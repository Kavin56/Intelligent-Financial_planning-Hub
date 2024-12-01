# 💰 Financial Planning Hub  

### 📜 Overview  
The **Financial Planning Hub** is a streamlined and user-friendly application designed to help you manage your finances effectively. From tracking expenses to generating insightful financial reports, this app is your all-in-one solution for financial planning.  

---

## ✨ Features  

### 🏠 **Home Module**  
- Welcomes users to the hub with a clean and interactive login interface.  
- Guides users on navigating the app's various features.  
- Enables user login and logout functionality.  

### 🧍 **Account Module**  
- **🔒 Secure Login/Signup**: User authentication using Firebase for secure access.  
- **🔑 Forgot Password**: Easy password recovery via email.  
- **👤 Session Management**: Keeps track of user details after login.  

### ➕ **Add Expenses Module**  
- **✍️ Manual Input**: Add expenses by selecting a category, amount, and description.  
- **📁 CSV Upload**: Bulk upload expenses using a CSV file.  
- **📢 Alerts**: Sends SMS notifications via Twilio when category thresholds are exceeded.  

### 📊 **Dashboard Module**  
- **📈 Interactive Charts**: Visualize spending trends with scatter plots, pie charts, and bar graphs.  
- **🧠 AI-Generated Reports**: Uses Google Generative AI to provide financial insights and savings suggestions.  
- **📄 PDF Export**: Download a beautifully formatted PDF report containing your data and insights.  

### 🔍 **View Expenses Module**  
- **📋 Expense Table**: View and filter expenses in an interactive table.  
- **🗑️ Deletion**: Remove specific expenses with just a few clicks.  

### ℹ️ **About Module**  
- Learn about the **Financial Planning Hub** and its purpose.  
- Detailed information about the app's features and benefits.  

---

## 🛠️ Technology Stack  

### 🐍 Backend  
- **Python**: The core language for the application.  
- **SQLite**: Lightweight database for storing expense data.  

### 🌐 Frontend  
- **Streamlit**: Interactive web interface for seamless user experience.  

### 🤖 APIs & Libraries  
- **Firebase**: Secure user authentication.  
- **Twilio**: SMS notifications for budget alerts.  
- **Google Generative AI**: AI-powered financial report generation.  
- **ReportLab**: PDF generation for financial reports.  
- **Matplotlib**: Data visualization for interactive charts.  

---

## 🚀 Getting Started  

### 🔧 Prerequisites  
1. Python 3.x installed on your system.  
2. Firebase credentials (`firebasekey.json`).  
3. `.env` file containing your API keys and configurations:  
   ```plaintext
   GOOGLE_GENAI_API_KEY=<your-google-genai-api-key>
   TWILIO_ACCOUNT_SID=<your-twilio-account-sid>
   TWILIO_AUTH_TOKEN=<your-twilio-auth-token>
   TWILIO_PHONE_NUMBER=<your-twilio-phone-number>
   USER_PHONE_NUMBER=<user-phone-number>
   analytics_tag=<your-google-analytics-tag>
   ```  

### 🖥️ Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Kavin56/Intelligent-Financial_planning-Hub.git
   cd financial-planning-hub
   ```  
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```  
3. Run the application:  
   ```bash
   streamlit run main.py
   ```  

---

## 📂 File Structure  

```plaintext
financial-planning-hub/
├── about.py            # About module
├── account.py          # User authentication and management
├── add_expenses.py     # Module for adding expenses
├── dashboard.py        # Financial dashboard with charts and reports
├── view_expenses.py    # View and delete expenses
├── home.py             # Welcome and login module
├── main.py             # Main application entry point
└── requirements.txt    # Python dependencies
```  

---

## 🛡️ Security & Privacy  
Your data is securely stored using Firebase and SQLite. Authentication ensures only authorized users can access their personal financial data.  

---

## 💡 Future Enhancements  
- **🔍 Advanced Filters**: Filter expenses by date range, category, or amount.  
- **📊 Custom Budgets**: Set custom spending limits for more categories.  
- **🌍 Multi-language Support**: Support for additional languages.  

---

## 🤝 Contributing  
Feel free to submit pull requests or open issues for any improvements or bugs.  

---

## 📧 Contact  
For any questions or feedback, email us at: **vskavinkumar2004@gmail.com**  

---  
