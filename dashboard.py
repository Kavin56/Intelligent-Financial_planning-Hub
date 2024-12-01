import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai
import os
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import tempfile
import re

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GOOGLE_GENAI_API_KEY")

# Configure Google Generative AI
genai.configure(api_key=api_key)

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

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO

# Function to save the report as PDF using ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO

# Function to save the report as PDF using ReportLab
def save_pdf(report, scatter_img_path, pie_img_path, bar_img_path):
    # Create a BytesIO buffer to save the PDF in memory
    pdf_output = BytesIO()
    
    # Create a canvas to draw the PDF content
    c = canvas.Canvas(pdf_output, pagesize=letter)
    width, height = letter
    
    # First page: Insert images (plots)
    c.setFont("Helvetica", 12)
    c.drawString(40, height - 40, "Financial Dashboard Plots")
    
    # Define the new larger size for each plot
    plot_width = 450
    plot_height = 180
    
    # Insert the images (charts) with increased size and adjusted Y positions
    # Adjusting the Y positions to raise the images higher
    c.drawImage(scatter_img_path, 40, height - 120 - plot_height, width=plot_width, height=plot_height, preserveAspectRatio=True)
    c.drawImage(pie_img_path, 40, height - 280 - plot_height, width=plot_width, height=plot_height, preserveAspectRatio=True)
    c.drawImage(bar_img_path, 40, height - 440 - plot_height, width=plot_width, height=plot_height, preserveAspectRatio=True)
    
    # Create a new page for the generated report
    c.showPage()

    # Second page: Insert the generated financial report text
    c.setFont("Helvetica", 10)
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 10)
    text.setTextOrigin(40, height - 60)  # Adjust starting position for the text

    # Add proper line spacing and better structure
    line_spacing = 14  # Increased line spacing for better readability
    text.setLeading(line_spacing)
    
    # Wrap and add the main report text
    lines = report.split('\n')
    
    # Loop through the lines and wrap the text
    for line in lines:
        wrapped_line = text_wrap(line, width - 80, c)  # Wrap each line based on width
        text.textLines(wrapped_line)  # Add the wrapped text to the PDF

    c.drawText(text)

    # Finalize the PDF
    c.showPage()
    c.save()

    # Rewind the buffer to the beginning
    pdf_output.seek(0)
    return pdf_output

# Helper function to wrap text based on the maximum width of the page
def text_wrap(text, max_width, c):
    # Create a list of wrapped lines that fit the page width
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # If the current line length + the next word exceeds the maximum width, start a new line
        if c.stringWidth(current_line + ' ' + word if current_line else word) > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += (' ' + word if current_line else word)
    
    if current_line:
        lines.append(current_line)
    
    return lines



# Function to save each plot as a temporary image file
def save_plot_as_temp_file(fig):
    # Create a temporary file to save the plot
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmpfile:
        fig.savefig(tmpfile, format='png')
        tmpfile.close()  # Close the file so it can be used later
        return tmpfile.name

# Streamlit UI
def app():
    st.subheader('Dashboard')

    # Check if the user is logged in
    if st.session_state.get('signedout') and st.session_state.get('username'):
        # User is logged in, display the dashboard
        st.success(f"Welcome, {st.session_state['username']}!")

        # Fetch expenses data from the database
        df = get_expenses_data()

        if df.empty:
            st.warning('No expense data available.')
            return

        # Scatter Plot (Amount vs Date)
        st.write('### Scatter Plot (Amount vs Date)')
        scatter_fig, scatter_ax = plt.subplots(figsize=(10, 6))
        categories = df['category'].unique()
        category_colors = {cat: plt.cm.viridis(i / len(categories)) for i, cat in enumerate(categories)}
        scatter_ax.scatter(
            df['date'], df['amount'], 
            c=df['category'].map(category_colors), 
            s=df['amount'] * 2, alpha=0.6
        )
        scatter_ax.set_xlabel('Date')
        scatter_ax.set_ylabel('Amount')
        scatter_ax.set_title('Scatter Plot of Spending Over Time')
        scatter_ax.legend(
            handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=cat)
                     for cat, color in category_colors.items()],
            title='Category'
        )
        st.pyplot(scatter_fig)
        scatter_img_path = save_plot_as_temp_file(scatter_fig)

        # Pie Chart (Proportions)
        st.write('### Pie Chart (Proportions)')
        category_sum = df.groupby('category')['amount'].sum()
        pie_fig, pie_ax = plt.subplots(figsize=(8, 6))
        pie_ax.pie(category_sum, labels=category_sum.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors[:len(category_sum)])
        pie_ax.set_title('Proportion of Spending by Category')
        st.pyplot(pie_fig)
        pie_img_path = save_plot_as_temp_file(pie_fig)

        # Bar Plot (Categorical Data)
        st.write('### Bar Plot (Categorical Data)')
        category_sum = df.groupby('category')['amount'].sum()
        bar_fig, bar_ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Paired(range(len(category_sum)))
        category_sum.plot(kind='bar', ax=bar_ax, color=colors)
        bar_ax.set_xlabel('Category')
        bar_ax.set_ylabel('Total Amount')
        bar_ax.set_title('Total Spending by Category')
        st.pyplot(bar_fig)
        bar_img_path = save_plot_as_temp_file(bar_fig)

        expenses_summary = df.groupby('category').agg(
            total_amount=('amount', 'sum'),
            expense_count=('amount', 'count')
        ).reset_index()

        expenses_summary_str = "\n".join([f"{row['category']}: Total - {row['total_amount']} | Count - {row['expense_count']}" for _, row in expenses_summary.iterrows()])

        salary = st.number_input("Enter your monthly salary:", min_value=0, step=1000)

        if st.button("Generate Financial Report"):
            if salary > 0:
                report = generate_report(salary, expenses_summary_str)
                st.text_area("Generated Report", value=report, height=300)
                pdf_output = save_pdf(report, scatter_img_path, pie_img_path, bar_img_path)
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_output,
                    file_name="financial_report.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("Please enter a valid salary.")
    else:
        # User is not logged in, show a warning
        st.warning("Please login to access the financial dashboard.")

# Run the Streamlit app
if __name__ == "__main__":
    app()
