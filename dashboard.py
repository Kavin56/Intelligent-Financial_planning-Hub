import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import re

# Set up the API key using environment variables
genai.configure(api_key="AIzaSyD-dLkR-ggyEHIMBAZ_34MJiBHQVfyxOAc")

# Create or connect to an SQLite database
conn = sqlite3.connect('expenses.db', check_same_thread=False)
c = conn.cursor()

# Retrieve expenses data from the database
def get_expenses_data():
    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)
    return df

# Function to remove unwanted symbols
def clean_report(report_text):
    # Remove symbols like *, #, and other non-alphanumeric characters
    cleaned_text = re.sub(r'[^\w\s.,!?]', '', report_text)  # Keep only letters, digits, and selected punctuation
    return cleaned_text

# Function to generate the financial report using Google Gemini
def generate_report(salary, expenses_summary):
    prompt = f"""
    I have the following expenses summary:
    {expenses_summary}

    My monthly salary is: {salary}

    Please create a financial report summarizing my expenses and how much I can save from my salary. Include insights on spending patterns, possible savings, and suggestions on managing finances better.
    """
    
    # Generate content using Google Gemini (model: gemini-1.5-flash)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    # Clean the report to remove unwanted symbols
    cleaned_report = clean_report(response.text)
    
    return cleaned_report

# Function to save the report as PDF using ReportLab
def save_pdf(report):
    # Create a BytesIO buffer to save the PDF in memory
    pdf_output = BytesIO()
    
    # Create a canvas to draw the PDF content
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter

    # Set font for the PDF
    c.setFont("Helvetica", 12)

    # Add text to the PDF (wrap text to avoid overflowing)
    text = c.beginText(40, height - 40)
    text.textLines(report)

    # Draw the text onto the canvas
    c.drawText(text)
    c.showPage()
    c.save()

    # Rewind the buffer to the beginning
    pdf_output.seek(0)
    return pdf_output

# Streamlit UI
def app():
    st.subheader('Dashboard')

    # Fetch expenses data from the database
    df = get_expenses_data()

    if df.empty:
        st.warning('No expense data available.')
        return

    # Scatter Plot (Amount vs Date)
    st.write('### Scatter Plot (Amount vs Date)')
    scatter_fig, scatter_ax = plt.subplots(figsize=(10, 6))
    
    # Define colors based on category
    categories = df['category'].unique()
    category_colors = {cat: plt.cm.viridis(i / len(categories)) for i, cat in enumerate(categories)}

    # Plotting scatter plot
    scatter_ax.scatter(
        df['date'], df['amount'], 
        c=df['category'].map(category_colors), 
        s=df['amount'] * 2, alpha=0.6  # Size of scatter points based on amount
    )
    scatter_ax.set_xlabel('Date')
    scatter_ax.set_ylabel('Amount')
    scatter_ax.set_title('Scatter Plot of Spending Over Time')

    # Add a legend for categories
    scatter_ax.legend(
        handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=cat)
                 for cat, color in category_colors.items()],
        title='Category'
    )
    st.pyplot(scatter_fig)

    # Pie Chart (Proportions)
    st.write('### Pie Chart (Proportions)')
    category_sum = df.groupby('category')['amount'].sum()
    pie_fig, pie_ax = plt.subplots(figsize=(8, 8))

    # Plotting the pie chart
    pie_ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors[:len(category_sum)])
    pie_ax.set_title('Proportion of Spending by Category')
    st.pyplot(pie_fig)

    # Bar Plot (Categorical Data)
    st.write('### Bar Plot (Categorical Data)')
    category_sum = df.groupby('category')['amount'].sum()

    bar_fig, bar_ax = plt.subplots(figsize=(10, 6))

    # Generate the colors from the Paired colormap and ensure it matches the number of categories
    colors = plt.cm.Paired(range(len(category_sum)))

    # Plotting the bar plot
    category_sum.plot(kind='bar', ax=bar_ax, color=colors)

    bar_ax.set_xlabel('Category')
    bar_ax.set_ylabel('Total Amount')
    bar_ax.set_title('Total Spending by Category')
    st.pyplot(bar_fig)

    # Automatically generate the expense summary
    expenses_summary = df.groupby('category').agg(
        total_amount=('amount', 'sum'),
        expense_count=('amount', 'count')
    ).reset_index()

    expenses_summary_str = "\n".join([f"{row['category']}: Total - {row['total_amount']} | Count - {row['expense_count']}" for _, row in expenses_summary.iterrows()])

    # Inputs: salary
    salary = st.number_input("Enter your monthly salary:", min_value=0, step=1000)

    if st.button("Generate Financial Report"):
        if salary > 0:
            # Generate the report using Google Gemini
            report = generate_report(salary, expenses_summary_str)
            st.text_area("Generated Report", value=report, height=300)

            # Save the report as a PDF using ReportLab
            pdf_output = save_pdf(report)

            # Provide a download button for the PDF
            st.download_button(
                label="Download Report as PDF",
                data=pdf_output,
                file_name="financial_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please enter a valid salary.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
