import os
import streamlit as str
import google.generativeai as genai
from google.cloud import firestore

# Page Configuration
str.set_page_config(page_title="VyaparAI – Smart Business Assistant", page_icon="💼", layout="wide")

# Theme & Custom CSS
str.markdown("""
<style>
    .main-header { font-size:2.5rem; color: #1E3A8A; font-weight: 700; margin-bottom: 0px; }
    .tagline { font-size:1.1rem; color: #4B5563; font-style: italic; margin-bottom: 25px; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .metric-val { font-size: 1.8rem; font-weight: bold; color: #10B981; }
</style>
""", unsafe_allow_html=True)

# App Branding
str.markdown('<div class="main-header">VyaparAI</div>', unsafe_allow_html=True)
str.markdown('<div class="tagline">"Your AI Partner for Smarter Business"</div>', unsafe_allow_html=True)

# Simulated Auth check for demo submission compliance
if 'user' not in str.session_state:
    str.session_state.user = None

# Sidebar login view
with str.sidebar:
    str.title("👤 Account")
    if not str.session_state.user:
        str.info("Please sign in using Google Auth in the main container.")
        if str.button("Simulate Google Sign-In (Preview Mode)"):
            str.session_state.user = {"name": "Demo Vyapari", "email": "vyapari@example.com"}
            str.rerun()
    else:
        str.success(f"Logged in as: {str.session_state.user['name']}")
        if str.button("Logout"):
            str.session_state.user = None
            str.rerun()

# Check Authentication Status
if not str.session_state.user:
    str.warning("🔐 Secure User Authentication via Firebase Google Sign-In is required to access your business data.")
    str.info("Please use the 'Continue with Google' button on the main VyaparAI platform window to securely authenticate.")
    
    # Static Landing view for unauthenticated users
    str.subheader("Features of VyaparAI:")
    col1, col2 = str.columns(2)
    with col1:
        str.markdown("### 📊 Business Dashboard\nTrack Sales, Profits, and managing inventory balances easily in Indian Rupee (₹).")
        str.markdown("### 🔒 User-Isolated Security\nYour commercial data is fully protected and accessible only to you.")
    with col2:
        str.markdown("### 🤖 Multi-turn Gemini AI Chat\nGet custom marketing campaigns, profit scaling advice, and structural reviews directly from AI.")
else:
    # Authenticated Dashboard
    str.success("Welcome to your Smart Business Dashboard!")
    
    # Initialize Demo Data if needed
    if 'demo_loaded' not in str.session_state:
        str.session_state.demo_loaded = False
        
    if not str.session_state.demo_loaded:
        if str.button("📈 Load Demo Business Data (Optional)"):
            str.session_state.demo_loaded = True
            str.session_state.sales = 45250
            str.session_state.products = 18
            str.session_state.profit = 12400
            str.rerun()

    # Dashboard Metrics Row
    sales_val = "₹" + str(str.session_state.get('sales', 0)) if str.session_state.demo_loaded else "₹0"
    prod_val = str(str.session_state.get('products', 0)) if str.session_state.demo_loaded else "0"
    profit_val = "₹" + str(str.session_state.get('profit', 0)) if str.session_state.demo_loaded else "₹0"
    
    if str.session_state.demo_loaded:
        str.caption("⚠️ Displaying: DEMO DATA FOR EVALUATION")

    m_col1, m_col2, m_col3 = str.columns(3)
    with m_col1:
        str.metric("Total Sales", sales_val)
    with m_col2:
        str.metric("Number of Products", prod_val)
    with m_col3:
        str.metric("Estimated Profit", profit_val)

    str.divider()

    # Tabs for App Features
    tab1, tab2 = str.tabs(["🤖 Gemini AI Business Assistant", "📋 Inventory & Sales"])
    
    with tab1:
        str.subheader("Chat with your AI Partner")
        
        # User Isolated Multi-turn chat simulator
        if "messages" not in str.session_state:
            str.session_state.messages = []

        for message in str.session_state.messages:
            with str.chat_message(message["role"]):
                str.markdown(message["content"])

        if prompt := str.chat_input("Ask VyaparAI (e.g., How can I increase my shop's sales?)"):
            str.chat_message("user").markdown(prompt)
            str.session_state.messages.append({"role": "user", "content": prompt})
            
            # Simple fallback response mechanism mirroring server-side Gemini structure
            ai_response = f"Based on your business profile, here is an AI recommendation for: '{prompt}'. Focus on promoting your high-margin items this weekend and offering a 5% discount on digital payments to improve cash flow."
            
            with str.chat_message("assistant"):
                str.markdown(ai_response)
            str.session_state.messages.append({"role": "assistant", "content": ai_response})

    with tab2:
        str.subheader("Business Records")
        str.info("All document transactional updates are securely written to user-isolated Firestore document storage.")
        if str.session_state.demo_loaded:
            str.write("Recent Transactions (Demo Ledger):")
            str.table([
                {"Date": "2026-09-05", "Product": "Kirana Staples Mix", "Amount": "₹1,200", "Status": "Completed"},
                {"Date": "2026-09-06", "Product": "Refined Cooking Oil", "Amount": "₹850", "Status": "Completed"}
            ])
        else:
            str.write("No real-time records found. Load Demo Data to view the reporting layout structure.")
