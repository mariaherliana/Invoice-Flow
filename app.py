import streamlit as st
import streamlit.components.v1 as components
import base64
import io
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="InvoiceFlow - Gmail Invoice Delivery",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define CSS styles
def load_css():
    st.markdown("""
    <style>
        :root {
            --primary: #4285F4;
            --secondary: #34A853;
            --background: #FAFAFA;
            --text: #202124;
            --accent: #EA4335;
            --success: #137333;
            --card-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
            --padding: 16px;
        }

        .main-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--padding) 0;
            margin-bottom: var(--padding);
        }

        .logo {
            display: flex;
            align-items: center;
            font-size: 24px;
            font-weight: 500;
            color: var(--primary);
        }

        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: var(--card-shadow);
            padding: var(--padding);
            margin-bottom: var(--padding);
        }

        .card-header {
            display: flex;
            align-items: center;
            margin-bottom: var(--padding);
            padding-bottom: var(--padding);
            border-bottom: 1px solid #E0E0E0;
        }

        .card-title {
            font-size: 18px;
            font-weight: 500;
            margin-left: 8px;
        }

        .contact-item {
            display: flex;
            align-items: center;
            padding: 8px;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }

        .contact-item:hover {
            background-color: #F1F3F4;
        }

        .contact-avatar {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            background-color: #DB4437;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 12px;
            font-weight: 500;
        }

        .contact-info {
            flex: 1;
        }

        .contact-name {
            font-weight: 500;
        }

        .contact-email {
            font-size: 12px;
            color: #5F6368;
        }

        .selected-contacts {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }

        .contact-chip {
            display: flex;
            align-items: center;
            background-color: #E8F0FE;
            color: var(--primary);
            border-radius: 16px;
            padding: 4px 8px;
            font-size: 14px;
        }

        .notification {
            padding: var(--padding);
            border-radius: 4px;
            margin-bottom: var(--padding);
            display: flex;
            align-items: center;
        }

        .notification.success {
            background-color: #E6F4EA;
            border-left: 4px solid var(--success);
        }

        .notification.error {
            background-color: #FCE8E6;
            border-left: 4px solid var(--accent);
        }

        .notification i {
            margin-right: 12px;
        }

        .notification.success i {
            color: var(--success);
        }

        .notification.error i {
            color: var(--accent);
        }

        .stButton > button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px 16px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }

        .stButton > button:hover {
            background-color: #3367D6;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {
            border: 1px solid #DDDDDD;
            border-radius: 4px;
        }

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2);
        }

        .stTabs [data-baseweb="tab-list"] {
            background-color: #F5F5F5;
            border-radius: 8px 8px 0 0;
            padding: 0 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 16px;
            font-weight: 500;
        }

        .stTabs [aria-selected="true"] {
            background-color: white;
            color: var(--primary);
            border-bottom: 2px solid var(--primary);
        }

        .stCheckbox > div {
            display: flex;
            align-items: center;
        }

        .stCheckbox > div > label {
            margin-left: 8px;
        }

        .file-uploader {
            border: 2px dashed #CCCCCC;
            border-radius: 8px;
            padding: 40px 20px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .file-uploader:hover {
            border-color: var(--primary);
            background-color: rgba(66, 133, 244, 0.05);
        }

        .invoice-preview {
            border: 1px solid #DDDDDD;
            border-radius: 4px;
            padding: var(--padding);
            margin-top: var(--padding);
        }

        .invoice-preview-content {
            height: 300px;
            background-color: #F5F5F5;
            border-radius: 4px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: #5F6368;
        }

        .payment-link {
            margin-top: var(--padding);
            padding: var(--padding);
            background-color: #F8F9FA;
            border-radius: 4px;
            border: 1px dashed #DDDDDD;
        }

        .settings-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }
    </style>
    """, unsafe_allow_html=True)

# Load the CSS
load_css()

# Initialize session state
if 'selected_contacts' not in st.session_state:
    st.session_state.selected_contacts = []
if 'invoice_uploaded' not in st.session_state:
    st.session_state.invoice_uploaded = False
if 'notification' not in st.session_state:
    st.session_state.notification = None

# Sample contact data
contacts = [
    {'id': 1, 'name': 'Alice Johnson', 'email': 'alice@example.com', 'company': 'Acme Inc'},
    {'id': 2, 'name': 'Bob Smith', 'email': 'bob@example.com', 'company': 'Tech Solutions'},
    {'id': 3, 'name': 'Charlie Brown', 'email': 'charlie@example.com', 'company': 'Creative Agency'},
    {'id': 4, 'name': 'Diana Prince', 'email': 'diana@example.com', 'company': 'Wonder Co'},
    {'id': 5, 'name': 'Ethan Hunt', 'email': 'ethan@example.com', 'company': 'Mission Impossible'},
    {'id': 6, 'name': 'Fiona Glenanne', 'email': 'fiona@example.com', 'company': 'Burn Notice'},
    {'id': 7, 'name': 'George Costanza', 'email': 'george@example.com', 'company': 'Seinfeld Inc'},
    {'id': 8, 'name': 'Hannah Montana', 'email': 'hannah@example.com', 'company': 'Disney'}
]

# Recent contacts
recent_contacts = [
    {'id': 9, 'name': 'Ian Fleming', 'email': 'ian@example.com', 'company': 'Bond Productions'},
    {'id': 10, 'name': 'Jane Austen', 'email': 'jane@example.com', 'company': 'Pride & Prejudice'},
    {'id': 11, 'name': 'Kevin McCallister', 'email': 'kevin@example.com', 'company': 'Home Alone'},
    {'id': 12, 'name': 'Laura Palmer', 'email': 'laura@example.com', 'company': 'Twin Peaks'}
]

# Email templates
email_templates = {
    'standard': """Dear [Customer Name],

Please find attached your invoice [Invoice Number] for [Service/Product] in the amount of [Amount].

Payment is due by [Due Date]. You can pay online using the link below or follow the payment instructions in the invoice.

Thank you for your business!

Best regards,
[Your Name]
[Your Company]""",
    'friendly': """Hi [Customer Name],

Hope you're doing well!

Just wanted to send over your invoice [Invoice Number] for the [Service/Product] we provided. The total comes to [Amount], and payment is due by [Due Date].

You can easily pay online through the link below. Let me know if you have any questions!

Thanks so much,
[Your Name]""",
    'formal': """Dear [Customer Name],

This email serves as notification that invoice [Invoice Number] has been generated for the [Service/Product] provided by [Your Company]. The total amount due is [Amount].

Payment is required by [Due Date]. Please refer to the attached invoice for detailed payment instructions, or utilize the online payment portal via the link provided below.

We appreciate your prompt attention to this matter.

Sincerely,
[Your Name]
[Your Title]
[Your Company]"""
}

# Helper functions
def show_notification(type, title, message):
    st.session_state.notification = {
        'type': type,
        'title': title,
        'message': message
    }

def toggle_contact_selection(contact):
    contact_ids = [c['id'] for c in st.session_state.selected_contacts]
    
    if contact['id'] in contact_ids:
        st.session_state.selected_contacts = [c for c in st.session_state.selected_contacts if c['id'] != contact['id']]
    else:
        st.session_state.selected_contacts.append(contact)

def get_initials(name):
    return ''.join([n[0] for n in name.split()])

def update_email_template(template_type):
    if template_type in email_templates:
        return email_templates[template_type]
    return email_templates['standard']

# Header
st.markdown("""
<div class="main-header">
    <div class="logo">
        <span style="font-size: 28px; margin-right: 8px;">📄</span>
        InvoiceFlow
    </div>
    <div style="display: flex; align-items: center;">
        <span>John Doe</span>
        <div style="width: 40px; height: 40px; border-radius: 50%; background-color: var(--primary); color: white; display: flex; align-items: center; justify-content: center; margin-left: var(--padding); cursor: pointer;">JD</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Display notification if exists
if st.session_state.notification:
    notification = st.session_state.notification
    icon = "✅" if notification['type'] == 'success' else "❌"
    
    st.markdown(f"""
    <div class="notification {notification['type']}">
        <span style="font-size: 24px;">{icon}</span>
        <div>
            <div style="font-weight: 500;">{notification['title']}</div>
            <div>{notification['message']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Clear notification after displaying
    st.session_state.notification = None

# Main content
col1, col2 = st.columns(2)

with col1:
    # Invoice Upload
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span style="font-size: 24px; color: var(--primary);">☁️</span>
            <h2 class="card-title">Upload Invoice</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Drag and drop your invoice PDF here or click to browse",
        type="pdf",
        key="invoice_file",
        help="Upload your invoice in PDF format"
    )
    
    if uploaded_file is not None:
        st.session_state.invoice_uploaded = True
        st.markdown(f"""
        <div class="invoice-preview">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--padding);">
                <div style="font-weight: 500;">Invoice Preview</div>
            </div>
            <div class="invoice-preview-content">
                <span style="font-size: 48px;">📄</span>
                <p>{uploaded_file.name}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contact Selection
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span style="font-size: 24px; color: var(--primary);">👥</span>
            <h2 class="card-title">Select Recipients</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Contact tabs
    tab1, tab2, tab3 = st.tabs(["Google Contacts", "Recent", "New Contact"])
    
    with tab1:
        search_query = st.text_input("Search contacts...", key="contact_search")
        
        # Filter contacts based on search query
        filtered_contacts = contacts
        if search_query:
            filtered_contacts = [
                c for c in contacts 
                if search_query.lower() in c['name'].lower() or search_query.lower() in c['email'].lower()
            ]
        
        # Display contacts
        for contact in filtered_contacts:
            is_selected = contact['id'] in [c['id'] for c in st.session_state.selected_contacts]
            
            st.markdown(f"""
            <div class="contact-item {'selected' if is_selected else ''}" onclick="toggle_contact_selection({contact['id']})">
                <div class="contact-avatar">{get_initials(contact['name'])}</div>
                <div class="contact-info">
                    <div class="contact-name">{contact['name']}</div>
                    <div class="contact-email">{contact['email']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {contact['name']}", key=f"select_{contact['id']}"):
                toggle_contact_selection(contact)
                st.rerun()
        
        # Display selected contacts
        if st.session_state.selected_contacts:
            st.markdown("**Selected Contacts:**")
            for contact in st.session_state.selected_contacts:
                st.markdown(f"""
                <div class="contact-chip">
                    {contact['name']}
                </div>
                """, unsafe_allow_html=True)
    
    with tab2:
        for contact in recent_contacts:
            is_selected = contact['id'] in [c['id'] for c in st.session_state.selected_contacts]
            
            st.markdown(f"""
            <div class="contact-item {'selected' if is_selected else ''}">
                <div class="contact-avatar">{get_initials(contact['name'])}</div>
                <div class="contact-info">
                    <div class="contact-name">{contact['name']}</div>
                    <div class="contact-email">{contact['email']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {contact['name']}", key=f"select_recent_{contact['id']}"):
                toggle_contact_selection(contact)
                st.rerun()
    
    with tab3:
        with st.form("new_contact_form"):
            name = st.text_input("Name")
            email = st.text_input("Email")
            company = st.text_input("Company (Optional)")
            
            submitted = st.form_submit_button("Add Contact")
            if submitted:
                if name and email:
                    new_contact = {
                        'id': len(contacts) + len(recent_contacts) + 1,
                        'name': name,
                        'email': email,
                        'company': company
                    }
                    toggle_contact_selection(new_contact)
                    st.rerun()
                else:
                    show_notification("error", "Missing Information", "Please provide at least a name and email address.")

with col2:
    # Email Composition
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span style="font-size: 24px; color: var(--primary);">✉️</span>
            <h2 class="card-title">Compose Email</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    email_subject = st.text_input("Subject", value="Invoice from Your Company")
    
    template_type = st.selectbox(
        "Email Template",
        ["Standard Invoice", "Friendly Reminder", "Formal Invoice", "Custom Template"],
        index=0
    )
    
    # Map template type to key
    template_key = "standard"
    if template_type == "Friendly Reminder":
        template_key = "friendly"
    elif template_type == "Formal Invoice":
        template_key = "formal"
    
    # Update email body based on template selection
    email_body = st.text_area(
        "Email Body",
        value=update_email_template(template_key),
        height=200
    )
    
    # Payment Link
    st.markdown("""
    <div class="payment-link">
    """, unsafe_allow_html=True)
    
    payment_provider = st.selectbox(
        "Payment Provider",
        ["Stripe", "PayPal", "Square", "No Payment Link"]
    )
    
    if payment_provider != "No Payment Link":
        payment_amount = st.text_input("Amount", placeholder="0.00")
        payment_description = st.text_input("Description", placeholder="Invoice #12345")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Send Time
    send_time = st.selectbox(
        "Send Time",
        ["Send Now", "Schedule for Later"]
    )
    
    if send_time == "Schedule for Later":
        # Default to tomorrow at 9 AM
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
        schedule_date = st.datetime_input("Schedule Date & Time", value=tomorrow)
    
    # Send button
    if st.button("Send Invoice", key="send_invoice"):
        if not st.session_state.selected_contacts:
            show_notification("error", "No Recipients", "Please select at least one recipient.")
        elif not st.session_state.invoice_uploaded:
            show_notification("error", "No Invoice", "Please upload an invoice.")
        else:
            # In a real application, you would send the invoice via Gmail API here
            show_notification("success", "Invoice Sent", "Your invoice has been sent successfully!")
            
            # Reset form
            st.session_state.invoice_uploaded = False
            st.session_state.selected_contacts = []
            st.rerun()
    
    # Email Settings
    st.markdown("""
    <div class="card">
        <div class="card-header">
            <span style="font-size: 24px; color: var(--primary);">⚙️</span>
            <h2 class="card-title">Email Settings</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    read_receipt = st.checkbox("Request read receipt")
    track_opens = st.checkbox("Track email opens", value=True)
    track_clicks = st.checkbox("Track link clicks", value=True)
    send_copy = st.checkbox("Send me a copy")

# Footer
st.markdown("""
<div style="text-align: center; padding: 20px; color: #5F6368; font-size: 14px;">
    © 2023 InvoiceFlow. All rights reserved.
</div>
""", unsafe_allow_html=True)
