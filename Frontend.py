# -- Install and setup Oracle Instant Client --
! wget -O oracleinstantclient.zip https://download.oracle.com/otn_software/linux/instantclient/19600/instantclient-basic-linux.x64-19.6.0.0.0dbru.zip
! unzip -oq oracleinstantclient.zip
! mkdir -p /opt/oracle
! mv instantclient_19_6 /opt/oracle/        #mv = move
! sh -c "echo /opt/oracle/instantclient_19_6 > /etc/ld.so.conf.d/oracle-instantclient.conf"
! ldconfig


# -- Include cx_Oracle package --
! pip install cx_Oracle

# Import cx_Oracle package and connect to Oracle Database
import cx_Oracle

HOST_NAME = "***"
PORT_NUMBER = "***"
SERVICE_NAME = "***"
USERNAME = "***"
PASSWORD = "***"

dsn_tns = cx_Oracle.makedsn(HOST_NAME, PORT_NUMBER, service_name=SERVICE_NAME)
conn = cx_Oracle.connect(user=USERNAME, password=PASSWORD, dsn=dsn_tns)

c = conn.cursor()   #connect to the database

from google.colab.widgets import TabBar
import ipywidgets as widgets
import time
import pandas as pd
from ipywidgets import interact, Text, DatePicker, IntText, Label, Dropdown, Checkbox
from datetime import date, datetime
import cx_Oracle
import hashlib
import os
from ipywidgets import Button, Label, Text, HTML, VBox, HBox, Dropdown, Textarea, Password, Output, Layout
import base64
import io
from IPython.display import display, clear_output, Image
import re  # For form validation
from IPython.display import HTML, display

# Define global CSS and design guidelines for consistent styling
# These variables will be used throughout the application
# Color scheme
PRIMARY_COLOR = '#4CAF50'    # Green for primary actions
SECONDARY_COLOR = '#2196F3'  # Blue for secondary actions
NEUTRAL_COLOR = '#f0f0f0'    # Light gray for neutral actions

# Function to create standard section headers
def create_header(text):
    styled_label = widgets.HTML(f"<div style='font-weight: bold; font-size: 17px; margin-bottom: 1px;'>{text}</div>")
    return styled_label

# Function to create standard section subheaders
SUBHEADER_STYLE = {'font_weight': 'bold', 'font_size': '13px', 'margin': '1px 0'}
def create_subheader(text):
    styled_label = widgets.HTML(f"""
    <div style='font-weight: {SUBHEADER_STYLE['font_weight']};
                 font-size: {SUBHEADER_STYLE['font_size']};
                 margin: {SUBHEADER_STYLE['margin']};'>
        {text}
    </div>
    """)
    return styled_label

# Function to create standard labels
def create_styled_label(text):
    return widgets.HTML(f"<div style='font-size: 13px;'>{text}</div>")

# Button layouts and styling
ACTION_BUTTON_LAYOUT = widgets.Layout(width='150px', margin='5px')
MENU_BUTTON_LAYOUT = widgets.Layout(width='250px', margin='5px')
SEARCH_BUTTON_LAYOUT = widgets.Layout(width='130px', margin='5px')

# Function to style buttons consistently
def style_button(button, color, is_bold=True):
    button.style.button_color = color
    if is_bold:
        button.style.font_weight = 'bold'
    return button

# Input field layouts
INPUT_LAYOUT = widgets.Layout(width='300px', border='1px solid #ccc', padding='5px')
DROPDOWN_LAYOUT = widgets.Layout(width='300px', border='1px solid #ccc')

# Section spacing
SECTION_SPACING = widgets.HTML("<br>")
SEPARATOR = widgets.HTML("<hr>")

# Define styles
STATUS_MSG_STYLE = {'font_weight': 'bold'}
ERROR_STYLE = {'color': 'red', 'font_weight': 'bold'}
SUCCESS_STYLE = {'color': 'green', 'font_weight': 'bold'}

def create_styled_message(text, status):
    if status == 'error':
        style = f"color: {ERROR_STYLE['color']}; font-weight: {ERROR_STYLE['font_weight']};"
    elif status == 'success':
        style = f"color: {SUCCESS_STYLE['color']}; font-weight: {SUCCESS_STYLE['font_weight']};"
    else:
        style = f"font-weight: {STATUS_MSG_STYLE['font_weight']};"

    return widgets.HTML(f"<div style='{style}'>{text}</div>")

tb_all = TabBar(['Introduction', 'Reg', 'ForgetPW', 'ResetPW', 'Member', 'Personal Details', 'Message', 'Shop Products', 'Shopping Cart', 'Checkout', 'Order Status', 'Details', 'Product Details', 'Order Details'])
# Global variables
reset_username = ""  # Used to pass username between forgot password and reset password pages
current_member = {'username': '', 'id': '', 'fname': '', 'lname': '', 'email': '', 'address': '', 'sec_q': '', 'sec_a': ''}

# Store password fields and their plain text equivalents
password_fields = []
checkbox = []

# Helper function to update welcome message consistently
def update_welcome_message(username):
  # Set welcome message with username prominently displayed with direct HTML styling
  member_welcome_label.value = f"<div style='font-weight: bold; font-size: 28px; color: #0066cc; margin: 15px 0; text-align: center;'>Welcome {username}!</div>"

# Function to toggle password visibility
def toggle_password_visibility(checkbox, password_field, plain_text_field):
  if checkbox.value == True:  # Checkbox is checked
    plain_text_field.value = password_field.value
    password_field.layout.display = 'none'
    plain_text_field.layout.display = ''
  else:  # Checkbox is unchecked
    password_field.value = plain_text_field.value
    plain_text_field.layout.display = 'none'
    password_field.layout.display = ''

# Main function to handle checkbox changes
def on_show_password_checkbox_change(change):
    # Identify which checkbox triggered the change
    checkbox_index = checkbox.index(change['owner'])
    toggle_password_visibility(checkbox[checkbox_index], password_fields[checkbox_index][0], password_fields[checkbox_index][1])

# Helper function to clear password fields and checkboxes
def clear_fields(*fields):
    for field in fields:
        if isinstance(field, widgets.Checkbox):
            field.value = False  # Reset checkbox
        else:
            field.value = ""  # Clear text fields

def showPage(tabName):
  # Clear fields when leaving specific tabs
  try:
    # Get current tab index (first time will raise AttributeError)
    current_tab_index = tb_all.output_tabs.index(tb_all.active_output)

    # Clear registration form when leaving Reg tab
    if tb_all.titles[current_tab_index] == "Reg" and tabName != "Reg":
      # Clear all registration fields
      Reg_textbox1.value = ""
      Reg_textbox2.value = ""
      Reg_textbox3.value = ""
      Reg_textbox4.value = ""
      Reg_textbox5.value = ""
      Reg_textbox6.value = ""
      Reg_textbox7.value = ""
      Reg_textbox8.value = ""
      Reg_cmb1.value = None
      username_taken_msg.value = ""
      Reg_label.value = "Please fill in the information below."

    # Clear forget password form when leaving ForgetPW tab
    elif tb_all.titles[current_tab_index] == "ForgetPW" and tabName != "ForgetPW":
      forgetPW_username_textbox.value = ""
      forgetPW_answer_textbox.value = ""
      forgetPW_status.value = ""
      forgetSec_status.value = ""

      # Reset visibility of form sections
      step2_label.layout.display = 'none'
      forgetPW_secq_label.layout.display = 'none'
      forgetPW_secq_display.layout.display = 'none'
      forgetPW_answer_textbox.layout.display = 'none'
      btnValidateAnswer.layout.display = 'none'

    # Clear reset password form when leaving ResetPW tab
    elif tb_all.titles[current_tab_index] == "ResetPW" and tabName != "ResetPW":
      ResetPW_password_textbox.value = ""
      ResetPW_confirm_textbox.value = ""
      ResetPW_status.value = ""
      ResetPW_requirements.value = "Password must be 1-16 characters long"

    # Clear login form when leaving Introduction tab
    elif tb_all.titles[current_tab_index] == "Introduction" and tabName != "Introduction":
      login_username_textbox.value = ""
      login_password_textbox.value = ""
      login_password_plaintext.value = ""
      login_show_password.value = False
      login_status.value = ""

    # Clear product detail status message when leaving Product Details tab
    elif tb_all.titles[current_tab_index] == "Product Details" and tabName != "Product Details":
      if 'product_detail_status' in globals():
        product_detail_status.value = ""

    # Clear sensitive payment information when leaving Checkout tab
    elif tb_all.titles[current_tab_index] == "Checkout" and tabName != "Checkout":
      if 'credit_card_textbox' in globals():
        credit_card_textbox.value = ""
      if 'expiry_date_textbox' in globals():
        expiry_date_textbox.value = ""
      if 'cvc_textbox' in globals():
        cvc_textbox.value = ""
      if 'checkout_status' in globals():
        checkout_status.value = ""

      # Reset trade-in section
      if 'has_tradein_checkbox' in globals():
        has_tradein_checkbox.value = False
      if 'tradein_devices' in globals():
        tradein_devices.clear()
      if 'tradein_devices_container' in globals():
        tradein_devices_container.layout.display = 'none'
      if 'add_tradein_btn' in globals():
        add_tradein_btn.layout.display = 'none'

  except Exception:
    # First run or other error, just proceed without clearing
    pass

  # Show the selected tab
  with tb_all.output_to(tabName):
    display()

  # Always refresh the Shop Products tab when it's shown to ensure up-to-date inventory
  if tabName == "Shop Products" and 'load_products' in globals():
    # If there's a search term active, refresh with that term
    if 'search_textbox' in globals() and search_textbox.value.strip():
      load_products(1, 5, search_textbox.value.strip())
    else:
      # Otherwise do a fresh load with no search term
      load_products(1, 5, "")

  # Clear fields when we enter a new tab, regardless of previous tab
  # This serves as a backup to ensure fields are always cleared

  # When going to a tab that is NOT Registration, make sure Registration fields are clear
  if tabName != "Reg" and 'Reg_textbox1' in globals():
    Reg_textbox1.value = ""
    Reg_textbox2.value = ""
    Reg_textbox3.value = ""
    Reg_textbox4.value = ""
    Reg_textbox5.value = ""
    Reg_textbox6.value = ""
    Reg_textbox7.value = ""
    Reg_textbox8.value = ""
    if 'Reg_cmb1' in globals():
      Reg_cmb1.value = None
    if 'username_taken_msg' in globals():
      username_taken_msg.value = ""
    if 'Reg_label' in globals():
      Reg_label.value = "Please fill in the information below."

  # When going to a tab that is NOT ForgetPW, make sure ForgetPW fields are clear
  if tabName != "ForgetPW" and 'forgetPW_username_textbox' in globals():
    forgetPW_username_textbox.value = ""
    if 'forgetPW_answer_textbox' in globals():
      forgetPW_answer_textbox.value = ""
    if 'forgetPW_status' in globals():
      forgetPW_status.value = ""
    if 'forgetSec_status' in globals():
      forgetSec_status.value = ""

    # Reset visibility of form sections
    if 'step2_label' in globals():
      step2_label.layout.display = 'none'
    if 'forgetPW_secq_label' in globals():
      forgetPW_secq_label.layout.display = 'none'
    if 'forgetPW_secq_display' in globals():
      forgetPW_secq_display.layout.display = 'none'
    if 'forgetPW_answer_textbox' in globals():
      forgetPW_answer_textbox.layout.display = 'none'
    if 'btnValidateAnswer' in globals():
      btnValidateAnswer.layout.display = 'none'

  # When going to a tab that is NOT ResetPW, make sure ResetPW fields are clear
  if tabName != "ResetPW" and 'ResetPW_password_textbox' in globals():
    ResetPW_password_textbox.value = ""
    if 'ResetPW_confirm_textbox' in globals():
      ResetPW_confirm_textbox.value = ""
    if 'ResetPW_status' in globals():
      ResetPW_status.value = ""
    if 'ResetPW_requirements' in globals():
      ResetPW_requirements.value = "Password must be 1-16 characters long"

  # When going to a tab that is NOT Introduction, make sure login fields are clear
  if tabName != "Introduction" and 'login_username_textbox' in globals():
    login_username_textbox.value = ""
    if 'login_password_textbox' in globals():
      login_password_textbox.value = ""
    if 'login_password_plaintext' in globals():
      login_password_plaintext.value = ""
    if 'login_show_password' in globals():
      login_show_password.value = False
    if 'login_status' in globals():
      login_status.value = ""

  # When going to a tab that is NOT Product Details, also ensure status is clear
  # This is a backup in case the first check fails
  if tabName != "Product Details" and 'product_detail_status' in globals():
    product_detail_status.value = ""

  # When going to a tab that is NOT Checkout, ensure sensitive payment information is cleared
  # This is a backup in case the first check fails
  if tabName != "Checkout":
    if 'credit_card_textbox' in globals():
      credit_card_textbox.value = ""
    if 'expiry_date_textbox' in globals():
      expiry_date_textbox.value = ""
    if 'cvc_textbox' in globals():
      cvc_textbox.value = ""
    if 'checkout_status' in globals():
      checkout_status.value = ""

    # Reset trade-in section
    if 'has_tradein_checkbox' in globals():
      has_tradein_checkbox.value = False
    if 'tradein_devices' in globals() and isinstance(tradein_devices, list):
      tradein_devices.clear()
    if 'tradein_devices_container' in globals():
      tradein_devices_container.layout.display = 'none'
    if 'add_tradein_btn' in globals():
      add_tradein_btn.layout.display = 'none'

##########################################################
################ Introduction Tab - Begin #################
##########################################################

with tb_all.output_to('Introduction'):
  # Create header
  intro_label = create_header("Welcome to Vincent Mobile!")

  # Create input fields with better visibility
  login_username_label = create_styled_label("Username:")
  login_username_textbox = Text(
    value='',
    placeholder='Enter your username',
    layout=widgets.Layout(width='250px', padding='5px', margin='5px')
  )

  login_password_label = create_styled_label("Password:")
  login_password_textbox = widgets.Password(
    value='',
    placeholder='Enter your password',
    layout=widgets.Layout(width='250px', padding='5px', margin='5px')
  )

  login_password_plaintext = Text(
    value='',
    placeholder='Enter your password',
    layout=widgets.Layout(width='250px', padding='5px', margin='5px')
  )

  # Initially hide the plain text password
  login_password_plaintext.layout.display = 'none'

  # Status message for login errors
  login_status = Label("")
  login_status.style = ERROR_STYLE

  # Create login button
  btnlogin = widgets.Button(description="Login", layout=ACTION_BUTTON_LAYOUT)
  style_button(btnlogin, PRIMARY_COLOR)

  # Checkbox to toggle password visibility
  login_show_password = widgets.Checkbox(
    description='Show password',
    value=False,
    disabled=False,
    indent=False
  )

  # First clear any existing entries to avoid duplicates
  checkbox = []
  password_fields = []

  # Then add the checkbox and password fields
  checkbox.append(login_show_password)
  password_fields.append((login_password_textbox, login_password_plaintext))

  # Now attach the observer
  login_show_password.observe(on_show_password_checkbox_change, names='value')

  # Registration and Reset sections with styled buttons
  intro_label1 = create_styled_label("Not a Member?")
  btnintro1 = widgets.Button(description="Register", layout=ACTION_BUTTON_LAYOUT)
  style_button(btnintro1, SECONDARY_COLOR)

  intro_label2 = create_styled_label("Forget Password?")
  btnintro2 = widgets.Button(description="Reset Password", layout=ACTION_BUTTON_LAYOUT)
  style_button(btnintro2, SECONDARY_COLOR)

  def on_btnlogin_clicked(b):
    username = login_username_textbox.value.strip()
    if not username:
      login_status.value = "Please enter your username."
      login_status.style = ERROR_STYLE
      return

    c.execute("SELECT M_PW, M_ID FROM MEMBER WHERE M_USERNAME = :username", {'username': username})
    result = c.fetchone()
    if result is None:
      login_status.value = "No username found."
      login_status.style = ERROR_STYLE
      return

    stored_password = result[0]
    member_id = result[1]  # Get the member ID from the query result

    # Get entered password from either password field or plaintext field
    # depending on which one is currently visible
    if login_password_textbox.layout.display == 'none':
      entered_password = login_password_plaintext.value
    else:
      entered_password = login_password_textbox.value

    if stored_password == entered_password:
      # Save current username and member ID for future reference
      current_member['username'] = username
      current_member['id'] = member_id  # Store the member ID

      # Set welcome message with username prominently displayed
      update_welcome_message(username)

      # Clear password fields and login form
      clear_fields(login_username_textbox, login_password_textbox,
                   login_password_plaintext, login_show_password)
      login_status.value = ""

      showPage("Member")
    else:
      login_status.value = "Wrong password."
      login_status.style = ERROR_STYLE
  btnlogin.on_click(on_btnlogin_clicked)

  def on_btnintro1_button_clicked(b):
    showPage("Reg")
  btnintro1.on_click(on_btnintro1_button_clicked)

  def on_btnintro2_button_clicked(b):
    showPage("ForgetPW")
  btnintro2.on_click(on_btnintro2_button_clicked)

  # Display the objects with a clearer layout
  display(widgets.VBox([
    widgets.Box([intro_label], layout=widgets.Layout(display='flex', justify_content='center', margin='20px 0')),
    SECTION_SPACING,

    # Username field with label
    widgets.VBox([
      login_username_label,
      login_username_textbox
    ], layout=widgets.Layout(margin='10px 0')),

    # Password field with label and visibility toggle
    widgets.VBox([
      login_password_label,
      widgets.HBox([login_password_textbox, login_password_plaintext]),
      widgets.Box([login_show_password], layout=widgets.Layout(margin='5px 0'))
    ], layout=widgets.Layout(margin='10px 0')),

    SECTION_SPACING,

    # Login button centered
    widgets.Box([btnlogin], layout=widgets.Layout(display='flex', justify_content='center', margin='20px 0')),

    # Error message area
    widgets.Box([login_status], layout=widgets.Layout(margin='10px 0', min_height='20px')),

    # Registration and password reset options
    widgets.Box([
      widgets.VBox([intro_label1, btnintro1]),
      widgets.VBox([intro_label2, btnintro2])
    ], layout=widgets.Layout(display='flex', justify_content='space-around', margin='20px 0'))

  ], layout=widgets.Layout(
    padding='30px',
    width='400px',
    margin='0 auto',
    border='1px solid #ddd',
    border_radius='5px'
  )))

################ Introduction Tab - End ################

##########################################################
################ Member Page - Begin ######################
##########################################################

with tb_all.output_to('Member'):
  # Welcome message with enhanced styling using the design pattern
  member_welcome_label = widgets.HTML("<div style='font-weight: bold; font-size: 28px; color: #0066cc; margin: 15px 0; text-align: center;'>Welcome to Vincent Mobile!</div>")
  member_options_label = create_subheader("What would you like to do?")

  # Create function buttons with consistent design
  btnViewPersonalDetails = widgets.Button(
      description="View/Edit Personal Details",
      style=widgets.ButtonStyle(button_color='#f5f5f5'),
      layout=widgets.Layout(width='100%', height='60px', margin='5px 0')
  )

  btnShop = widgets.Button(
      description="Shop Products",
      style=widgets.ButtonStyle(button_color='#f5f5f5'),
      layout=widgets.Layout(width='100%', height='60px', margin='5px 0')
  )

  btnViewCart = widgets.Button(
      description="View Shopping Cart",
      style=widgets.ButtonStyle(button_color='#f5f5f5'),
      layout=widgets.Layout(width='100%', height='60px', margin='5px 0')
  )

  btnOrderHistory = widgets.Button(
      description="Order History",
      style=widgets.ButtonStyle(button_color='#f5f5f5'),
      layout=widgets.Layout(width='100%', height='60px', margin='5px 0')
  )

  btnLogout = widgets.Button(
      description="Logout",
      style=widgets.ButtonStyle(button_color='#f5f5f5'),
      layout=widgets.Layout(width='100%', height='60px', margin='5px 0')
  )

  # Button handlers stay the same
  def on_btnViewPersonalDetails_clicked(b):
    setup_personal_details()
    showPage("Personal Details")
  btnViewPersonalDetails.on_click(on_btnViewPersonalDetails_clicked)

  def on_btnOrderHistory_clicked(b):
    if 'order_system' in globals():
      globals()['order_system'].display_member_orders(current_member)
      showPage("Order Status")
    else:
      print("Order system not initialized yet.")
  btnOrderHistory.on_click(on_btnOrderHistory_clicked)

  def on_btnShop_clicked(b):
    showPage("Shop Products")
  btnShop.on_click(on_btnShop_clicked)

  def on_btnViewCart_clicked(b):
    setup_shopping_cart()
    showPage("Shopping Cart")
  btnViewCart.on_click(on_btnViewCart_clicked)

  def on_btnLogout_clicked(b):
    for key in current_member:
      current_member[key] = ''
    login_username_textbox.value = ""
    login_password_textbox.value = ""
    login_status.value = ""
    showPage("Introduction")
  btnLogout.on_click(on_btnLogout_clicked)

  # Create a container for all buttons with a clean layout
  options_section = widgets.VBox([
    btnViewPersonalDetails,
    btnShop,
    btnViewCart,
    btnOrderHistory,
    btnLogout
  ], layout=widgets.Layout(
    width='450px',
    margin='0 auto'
  ))

  # Display with the clean layout
  display(widgets.VBox([
    member_welcome_label,
    options_section
  ]))

##########################################################
################ Register Tab - Begin ######################
##########################################################

with tb_all.output_to('Reg'):

  Reg_label = Label("Please fill in the information below.")

  # Add clear notification about username
  Reg_username_notice = Label("Note: Your username CANNOT be changed after registration.")


#gender, hkid, dob/age
  Reg_label1 = Label("Username: ")
  Reg_textbox1 = Text(value='', placeholder='Username', disabled=False)

  # Username error message that appears next to the input
  username_taken_msg = Label("")

  Reg_label2 = Label("Password: ")
  # Create regular text fields for password (no masking)
  Reg_textbox2 = Text(value='', placeholder='Password', disabled=False)
  Reg_label3 = Label("Retype Password: ")
  # Create regular text field for password confirmation (no masking)
  Reg_textbox3 = Text(value='', placeholder='Retype Password', disabled=False)

  # No password visibility needed for registration
  # Keep the checkbox for UI consistency but don't connect it to any functionality
  Reg_show_password = widgets.Checkbox(
    value=False,
    description='Show passwords',
    disabled=True,  # Disabled since we're not using password masking
    indent=False
  )

  # No need to store password fields for the registration page
  checkbox.append(Reg_show_password)
  Reg_show_password.observe(on_show_password_checkbox_change, names='value')


  Reg_label4 = Label("First Name: ")
  Reg_textbox4 = Text(value='', placeholder='First Name', disabled=False)
  Reg_label5 = Label("Last Name: ")
  Reg_textbox5 = Text(value='', placeholder='Last Name', disabled=False)
  Reg_label6 = Label("Email: ")
  Reg_textbox6 = Text(value='', placeholder='Email', disabled=False)
  Reg_label7 = Label("Address: ")
  Reg_textbox7 = Text(value='', placeholder='Address', disabled=False)
    #District and Country?
  Reg_label8 = Label("Security Question: ")
  Reg_cmb1 = widgets.Dropdown(options=["What is your oldest sibling's middle name?", "What was the first concert you attended?", "What was the make and model of your first car?", "Who is your primary school principal?"], value=None)
  Reg_label9 = Label("Security Answer: ")
  Reg_textbox8 = Text(value='', placeholder='Answer for Security Question', disabled=False)

  btnReg = widgets.Button(description="Finish Registration")
  btnReg1 = widgets.Button(description="Clear all")
  Reg_label10 = Label("Already a member?")
  btnReg2 = widgets.Button(description="Login")

  # Style buttons using the global styling function
  style_button(btnReg, PRIMARY_COLOR)
  style_button(btnReg1, NEUTRAL_COLOR, is_bold=False)
  style_button(btnReg2, SECONDARY_COLOR)

  def on_btnReg_button_clicked(b):
    # First, check if the username is empty or too long
    if len(Reg_textbox1.value) <= 0:
      Reg_label.value = "Please enter Username."
      return
    elif len(Reg_textbox1.value) > 10:
      Reg_label.value = "Please enter Username with less than 10 characters."
      return

    # Check if username is already in use before proceeding with other validations
    # This way users don't waste time filling out the whole form if the username is taken
    try:
      c.execute("SELECT M_USERNAME FROM MEMBER WHERE M_USERNAME = :username", {'username': Reg_textbox1.value})
      if c.fetchone() is not None:
        # Display error message next to username field
        username_taken_msg.value = "Username already taken. Try another."
        # Keep focus on the username field
        return
      else:
        # Clear any previous error message
        username_taken_msg.value = ""
    except Exception as e:
      Reg_label.value = f"Database error: {str(e)}"
      return

    # Get password values directly
    password = Reg_textbox2.value
    confirm_password = Reg_textbox3.value

    # Continue with other validations
    if len(password) <= 0:
      Reg_label.value = "Please enter password."
      return
    elif len(password) > 16:
      Reg_label.value = "Please enter password with less than 16 characters."
      return
    elif confirm_password != password:
      Reg_label.value = "Password inconsistent. Please re-enter."
      return

    if len(Reg_textbox4.value) <= 0:
      Reg_label.value = "Please enter your first name."
      return
    elif len(Reg_textbox4.value) > 20:
      Reg_label.value = "Please enter first name less than 20 characters, or contact our staff for any enquiries."
      return

    if len(Reg_textbox5.value) <= 0:
      Reg_label.value = "Please enter your last name."
      return
    elif len(Reg_textbox5.value) > 20:
      Reg_label.value = "Please enter last name less than 20 characters, or contact our staff for any enquiries."
      return

    if len(Reg_textbox6.value) <= 0:
      Reg_label.value = "Please enter email."
      return
    elif len(Reg_textbox6.value) > 30:
      Reg_label.value = "Please enter email less than 30 characters."
      return
    elif "@" not in str(Reg_textbox6.value) or "." not in str(Reg_textbox6.value):
      Reg_label.value = "Invalid email. Please re-enter."
      return

    if len(Reg_textbox7.value) <= 0:
      Reg_label.value = "Please enter address."
      return
    elif len(Reg_textbox7.value) > 100:
      Reg_label.value = "Address too long."
      return

    if Reg_cmb1.value == None:
      Reg_label.value = "Please choose your security question."
      return

    if len(Reg_textbox8.value) <= 0:
      Reg_label.value = "Please enter your answer for security question."
      return
    elif len(Reg_textbox8.value) > 30:
      Reg_label.value = "Please enter your answer within 30 characters."
      return

    # Check username availability one more time
    try:
      c.execute("SELECT M_USERNAME FROM MEMBER WHERE M_USERNAME = :username", {'username': Reg_textbox1.value})
      if c.fetchone() is not None:
        # Display error message next to username field
        username_taken_msg.value = "Username already taken. Try another."
        return

      # If we get here, the username is available, proceed with registration
      M_ID_query = "SELECT COUNT(*) FROM MEMBER"
      c.execute(M_ID_query)
      M_ID = c.fetchone()[0]+1

      Reg_date_query = "SELECT TO_CHAR(SYSDATE, 'dd/mon/yyyy') FROM DUAL"
      c.execute(Reg_date_query)
      Reg_date = c.fetchone()[0]

      insert_query = """
      INSERT INTO MEMBER (M_ID, M_USERNAME, M_PW, FNAME, LNAME, M_EMAIL, M_ADDRESS, REG_DATE, M_SEC_Q, M_SEC_A)
      VALUES (:M_ID, :M_USERNAME, :M_PW, :FNAME, :LNAME, :M_EMAIL, :M_ADDRESS, :REG_DATE, :M_SEC_Q, :M_SEC_A)
      """
      values = {
      'M_ID': M_ID,
      'M_USERNAME': Reg_textbox1.value,
      'M_PW': password,
      'FNAME': Reg_textbox4.value,
      'LNAME': Reg_textbox5.value,
      'M_EMAIL': Reg_textbox6.value,
      'M_ADDRESS': Reg_textbox7.value,
      'REG_DATE': Reg_date,
      'M_SEC_Q': Reg_cmb1.value,
      'M_SEC_A': Reg_textbox8.value
      }

      try:
        c.execute(insert_query, values)
        c.execute("commit")
        btnReg.disabled = True

        # Clear all registration fields
        Reg_textbox1.value = ""
        Reg_textbox2.value = ""
        Reg_textbox3.value = ""
        Reg_textbox4.value = ""
        Reg_textbox5.value = ""
        Reg_textbox6.value = ""
        Reg_textbox7.value = ""
        Reg_textbox8.value = ""
        Reg_cmb1.value = None
        username_taken_msg.value = ""
        Reg_label.value = "Please fill in the information below."

        # Set success message for Message page with updated title
        message_title.value = "Registration Successful!"
        message_label.value = "Your account has been created. You can now log in with your new credentials."

        # Update message context and button text
        message_context['return_to_login'] = True
        message_back_button.description = "Back to Login"
        message_back_button.style.button_color = '#2196F3'  # Blue button for login action

        # Show message page
        showPage("Message")
      except Exception as e:
        print(f"An error occurred: {e}")
        Reg_label.value = f"Registration failed: {str(e)}"
        Reg_label.style = {'color': 'red', 'font_weight': 'bold'}
        try:
          conn.rollback()
        except:
          pass
    except Exception as e:
      Reg_label.value = f"Error checking username: {str(e)}"

  btnReg.on_click(on_btnReg_button_clicked)

  def on_btnReg1_button_clicked(b):
    # Clear all form fields
    Reg_textbox1.value = ""
    Reg_textbox2.value = ""
    Reg_textbox3.value = ""
    Reg_textbox4.value = ""
    Reg_textbox5.value = ""
    Reg_textbox6.value = ""
    Reg_textbox7.value = ""
    Reg_textbox8.value = ""
    Reg_cmb1.value = None

    # Also clear any error messages
    username_taken_msg.value = ""
    Reg_label.value = "Please fill in the information below."
  btnReg1.on_click(on_btnReg1_button_clicked)

  def on_btnReg2_button_clicked(b):
    showPage("Introduction")
  btnReg2.on_click(on_btnReg2_button_clicked)

  # Create consistent widths for the layout
  label_width = '150px'
  field_width = '500px'

  # Set fixed widths for all labels and input fields
  for label in [Reg_label1, Reg_label2, Reg_label3, Reg_label4, Reg_label5, Reg_label6, Reg_label7, Reg_label8, Reg_label9]:
    label.layout.width = label_width

  for field in [Reg_textbox1, Reg_textbox2, Reg_textbox3, Reg_textbox4, Reg_textbox5, Reg_textbox6, Reg_textbox7, Reg_textbox8]:
    field.layout.width = field_width

  Reg_cmb1.layout.width = field_width

  # Add a divider for visual separation
  divider = widgets.HTML("<hr style='border-top: 1px dashed #ccc; margin: 20px 0;'>")

  # Create a better header
  header = widgets.HTML("<h2>Your Registration Details</h2>")
  instructions = widgets.HTML("<p>View and complete all fields below to register. Username cannot be changed once registered.</p>")
  instructions2 = widgets.HTML("<p>Complete all fields and click 'Finish Registration' when done.</p>")

  # Display the registration form with improved layout
  display(widgets.VBox([
    header,
    instructions,
    instructions2,
    divider,
    widgets.HBox([Reg_label1, Reg_textbox1, username_taken_msg]),
    widgets.HBox([Reg_label2, Reg_textbox2]),
    widgets.HBox([Reg_label3, Reg_textbox3]),
    widgets.HBox([Reg_label4, Reg_textbox4]),
    widgets.HBox([Reg_label5, Reg_textbox5]),
    widgets.HBox([Reg_label6, Reg_textbox6]),
    widgets.HBox([Reg_label7, Reg_textbox7]),
    widgets.HBox([Reg_label8, Reg_cmb1]),
    widgets.HBox([Reg_label9, Reg_textbox8]),
    widgets.HTML("<br>"),
    widgets.HBox([btnReg, btnReg1]),
    widgets.HTML("<hr>"),
    widgets.HBox([Reg_label10, btnReg2])
  ]))

  ################ Register - End ################

##########################################################
################ ForgetPW Tab - Begin ######################
##########################################################

with tb_all.output_to('ForgetPW'):

  forgetPW_title = create_header("Reset Your Password")
  forgetPW_status = Label("")
  forgetSec_status = Label ("")

  # Step 1: Username entry
  step1_label = Label("Step 1: Enter your username")
  forgetPW_username_label = Label("Username: ")
  forgetPW_username_textbox = Text(value='', placeholder="Enter Username", disabled=False)
  btnGetSecQuestion = widgets.Button(description="Find Account")

  # Style button using global styling
  style_button(btnGetSecQuestion, PRIMARY_COLOR)

  # Step 2: Security question (initially hidden)
  step2_label = Label("Step 2: Answer security question")
  step2_label.layout.display = 'none'

  # Changed to a Label instead of a Text widget
  forgetPW_secq_label = Label("Security Question:")
  forgetPW_secq_label.layout.display = 'none'

  # Separate label to display the question
  forgetPW_secq_display = Label("")
  forgetPW_secq_display.style = {'font_weight': 'bold', 'font_size': '14px'}
  forgetPW_secq_display.layout.display = 'none'

  forgetPW_answer_textbox = Text(value='', placeholder="Your Answer", disabled=False)
  forgetPW_answer_textbox.layout.display = 'none'
  btnValidateAnswer = widgets.Button(description="Validate Answer")
  btnValidateAnswer.layout.display = 'none'

  # Style button using global styling
  style_button(btnValidateAnswer, PRIMARY_COLOR)

  # Variables to store data
  sec_question_data = {'question': '', 'answer': '', 'username': ''}

  def on_btnGetSecQuestion_clicked(b):
    username = forgetPW_username_textbox.value
    if len(username) <= 0:
      forgetPW_status.value = "Please enter your username."
      return

    c.execute("SELECT M_SEC_Q, M_SEC_A FROM MEMBER WHERE M_USERNAME = :username", {'username': username})
    result = c.fetchone()
    if result is None:
      forgetPW_status.value = "No username found."
      return

    # Store security data
    security_question, answer = result
    sec_question_data['question'] = security_question
    sec_question_data['answer'] = answer
    sec_question_data['username'] = username

    # Update UI to show security question
    forgetPW_secq_display.value = security_question
    forgetSec_status.value = "Please answer your security question."

    # Show step 2 elements
    step2_label.layout.display = 'block'
    forgetPW_secq_label.layout.display = 'block'
    forgetPW_secq_display.layout.display = 'block'
    forgetPW_answer_textbox.layout.display = 'block'
    btnValidateAnswer.layout.display = 'block'

  btnGetSecQuestion.on_click(on_btnGetSecQuestion_clicked)

  def on_btnValidateAnswer_clicked(b):
    user_answer = forgetPW_answer_textbox.value
    if len(user_answer) <= 0:
      forgetSec_status.value = "Please answer the security question."
      return

    if user_answer.lower() != sec_question_data['answer'].lower():
      forgetSec_status.value = "Wrong answer, please try again or contact our staff for any enquiries."
      return

    # Correct answer, proceed to password reset
    forgetSec_status.value = "Answer verified. You can now reset your password."
    # Store username for password reset page
    global reset_username
    reset_username = sec_question_data['username']
    showPage("ResetPW")

  btnValidateAnswer.on_click(on_btnValidateAnswer_clicked)

  # Back to login button
  btnBackToLogin = widgets.Button(description="Back to Login")
  # Style button using global styling
  style_button(btnBackToLogin, SECONDARY_COLOR)

  def on_btnBackToLogin_clicked(b):
    showPage("Introduction")

  btnBackToLogin.on_click(on_btnBackToLogin_clicked)

  # Layout
  title_box = widgets.HBox([forgetPW_title])
  status_box = widgets.HBox([forgetPW_status])
  status2_box = widgets.HBox([forgetSec_status])

  step1_box = widgets.HBox([step1_label])
  username_box = widgets.HBox([forgetPW_username_label, forgetPW_username_textbox])
  find_btn_box = widgets.HBox([btnGetSecQuestion])

  step2_box = widgets.HBox([step2_label])
  secq_box = widgets.VBox([
    forgetPW_secq_label,
    forgetPW_secq_display
  ])
  answer_box = widgets.HBox([forgetPW_answer_textbox])
  validate_btn_box = widgets.HBox([btnValidateAnswer])

  back_btn_box = widgets.HBox([btnBackToLogin])

  display(widgets.VBox([
    title_box,
    widgets.HTML("<hr>"),
    step1_box,
    username_box,
    find_btn_box,
    status_box,
    widgets.HTML("<hr>"),
    step2_box,
    status2_box,
    secq_box,
    answer_box,
    validate_btn_box,
    back_btn_box
  ]))

################ ForgetPW - End ################


##########################################################
################ ResetPW Tab - Begin ######################
##########################################################

with tb_all.output_to('ResetPW'):

  ResetPW_title = create_header("Reset Your Password")
  ResetPW_status = Label("")

  # Username display
  ResetPW_username_label = Label("Username: ")
  ResetPW_username_display = Label("") # Will be filled when page is shown


  # Password fields - no masking (using regular Text fields instead of Password fields)
  ResetPW_password_label = Label("Enter new password: ")
  ResetPW_password_textbox = widgets.Text(value='', placeholder="New password", disabled=False)
  ResetPW_confirm_label = Label("Confirm new password: ")
  ResetPW_confirm_textbox = widgets.Text(value='', placeholder="Retype password", disabled=False)

  # Password requirements info
  ResetPW_requirements = Label("Password must be 1-16 characters long")

  # Reset button
  btnResetPassword = widgets.Button(description="Reset Password")
  # Style button using global styling
  style_button(btnResetPassword, PRIMARY_COLOR)

  # Back button
  btnBackToLogin = widgets.Button(description="Back to Login")
  # Style button using global styling
  style_button(btnBackToLogin, SECONDARY_COLOR)

  # Function to clear status messages
  def clear_resetpw_status():
    ResetPW_status.value = ""
    ResetPW_requirements.value = "Password must be 1-16 characters long"

  def on_btnResetPassword_clicked(b):
    # Clear status messages first
    clear_resetpw_status()

    # Get password values directly from the password fields
    password = ResetPW_password_textbox.value
    confirm_password = ResetPW_confirm_textbox.value

    if len(password) <= 0:
        ResetPW_status.value = "Please enter a password."
    elif len(password) > 16:
        ResetPW_requirements.value = "Password must be less than 16 characters."

    elif password != confirm_password:
        ResetPW_requirements.value = "Passwords don't match. Please try again."

    else:
      try:
        c.execute(
          "UPDATE MEMBER SET M_PW = :new_password WHERE M_USERNAME = :username",
          {'new_password': password, 'username': reset_username}
        )
        c.execute("commit")

        # Set success message for Message page with updated title
        message_title.value = "Password Reset Successful!"
        message_label.value = "Your password has been updated. You can now log in with your new password."

        # Update message context and button text
        message_context['return_to_login'] = True
        message_back_button.description = "Back to Login"
        message_back_button.style.button_color = '#2196F3'  # Blue button for login action

        # Show message page
        showPage("Message")
      except Exception as e:
        ResetPW_status.value = f"An error occurred: {e}"
        try:
          c.execute("rollback")
        except:
          pass

  btnResetPassword.on_click(on_btnResetPassword_clicked)

  def on_btnBackToLogin_clicked(b):
    # Clear status messages before leaving the page
    clear_resetpw_status()
    showPage("Introduction")

  btnBackToLogin.on_click(on_btnBackToLogin_clicked)

  # Update username display when page is shown
  def on_reset_pw_shown():
    ResetPW_username_display.value = reset_username
    # Clear any status messages when page is shown
    clear_resetpw_status()

  # Layout
  title_box = widgets.HBox([ResetPW_title])
  status_box = widgets.HBox([ResetPW_status])
  username_box = widgets.HBox([ResetPW_username_label, ResetPW_username_display])
  password_box = widgets.HBox([ResetPW_password_label, ResetPW_password_textbox])
  confirm_box = widgets.HBox([ResetPW_confirm_label, ResetPW_confirm_textbox])
  requirements_box = widgets.HBox([ResetPW_requirements])
  buttons_box = widgets.HBox([btnResetPassword, btnBackToLogin])

  # Call this function when the tab is displayed
  on_reset_pw_shown()

  display(widgets.VBox([
    title_box,
    status2_box,
    widgets.HTML("<hr>"),
    username_box,
    password_box,
    confirm_box,
    requirements_box,
    buttons_box
  ]))

################ ResetPW - End ################

################ Personal Details ################

with tb_all.output_to('Personal Details'):

  # Create title and subtitle with better styling
  PD_title_label = create_header("Your Personal Details")
  PD_subtitle_label = Label("View and edit your personal information below. Username cannot be changed.")
  PD_instructions = Label("Make changes to any field and click 'Save Changes' when finished.")

  # Create a separator line
  PD_spacer = Label("---------------------------------------------------------------------------------------------------------------------------------")

  # Create labels and input fields
  PD_id_label = Label("Member ID: ")
  PD_id_textbox = Text(value='', disabled=True)

  PD_username_label = Label("Username: ")
  PD_username_textbox = Text(value='', disabled=True)
  PD_username_notice = Label("(Cannot be changed)")
  PD_username_notice.style = { 'font_style': 'italic'}

  PD_fname_label = Label("First Name: ")
  PD_fname_textbox = Text(value='', disabled=False)

  PD_lname_label = Label("Last Name: ")
  PD_lname_textbox = Text(value='', disabled=False)

  PD_email_label = Label("Email: ")
  PD_email_textbox = Text(value='', disabled=False)

  PD_address_label = Label("Address: ")
  PD_address_textbox = Text(value='', disabled=False)

  PD_sec_q_label = Label("Security Question: ")
  PD_sec_q_dropdown = Dropdown(
    options=["What is your oldest sibling's middle name?",
             "What was the first concert you attended?",
             "What was the make and model of your first car?",
             "Who is your primary school principal?"],
    value=None,
    disabled=False
  )

  PD_sec_a_label = Label("Security Answer: ")
  PD_sec_a_textbox = Text(value='', disabled=False)

  # Status message
  PD_status_msg = Label("")

  # Create buttons
  PD_update_button = widgets.Button(description="Save Changes")
  style_button(PD_update_button, PRIMARY_COLOR)

  PD_reset_button = widgets.Button(description="Reset Form")
  style_button(PD_reset_button, NEUTRAL_COLOR)

  PD_back_button = widgets.Button(description="Back to Menu")
  style_button(PD_back_button, SECONDARY_COLOR)

  # Define button handlers
  def on_PD_update_button_clicked(b):
    # Validate inputs
    if len(PD_fname_textbox.value) <= 0:
      PD_status_msg.value = "First name cannot be empty."
      return
    elif len(PD_fname_textbox.value) > 20:
      PD_status_msg.value = "First name must be less than 20 characters."
      return

    if len(PD_lname_textbox.value) <= 0:
      PD_status_msg.value = "Last name cannot be empty."
      return
    elif len(PD_lname_textbox.value) > 20:
      PD_status_msg.value = "Last name must be less than 20 characters."
      return

    if len(PD_email_textbox.value) <= 0:
      PD_status_msg.value = "Email cannot be empty."
      return
    elif len(PD_email_textbox.value) > 30:
      PD_status_msg.value = "Email must be less than 30 characters."
      return
    elif "@" not in PD_email_textbox.value or "." not in PD_email_textbox.value:
      PD_status_msg.value = "Please enter a valid email address."
      return

    if len(PD_address_textbox.value) <= 0:
      PD_status_msg.value = "Address cannot be empty."
      return
    elif len(PD_address_textbox.value) > 100:
      PD_status_msg.value = "Address is too long."
      return

    if PD_sec_q_dropdown.value is None:
      PD_status_msg.value = "Please select a security question."
      return

    if len(PD_sec_a_textbox.value) <= 0:
      PD_status_msg.value = "Security answer cannot be empty."
      return
    elif len(PD_sec_a_textbox.value) > 30:
      PD_status_msg.value = "Security answer must be less than 30 characters."
      return

    try:
      # Update member details in database
      update_query = """
      UPDATE MEMBER
      SET FNAME = :fname,
          LNAME = :lname,
          M_EMAIL = :email,
          M_ADDRESS = :address,
          M_SEC_Q = :sec_q,
          M_SEC_A = :sec_a
      WHERE M_ID = :id
      """

      values = {
        'fname': PD_fname_textbox.value,
        'lname': PD_lname_textbox.value,
        'email': PD_email_textbox.value,
        'address': PD_address_textbox.value,
        'sec_q': PD_sec_q_dropdown.value,
        'sec_a': PD_sec_a_textbox.value,
        'id': PD_id_textbox.value
      }

      c.execute(update_query, values)
      c.execute("commit")

      # Update current_member variable
      current_member['fname'] = PD_fname_textbox.value
      current_member['lname'] = PD_lname_textbox.value
      current_member['email'] = PD_email_textbox.value
      current_member['address'] = PD_address_textbox.value
      current_member['sec_q'] = PD_sec_q_dropdown.value
      current_member['sec_a'] = PD_sec_a_textbox.value

      # Show success message directly on the page
      PD_status_msg.value = "Your details have been updated successfully!"
      PD_status_msg.style = { 'font_weight': 'bold'}
      # Stay on the same page to show the updated details
    except Exception as e:
      PD_status_msg.value = f"Error updating details: {str(e)}"
      try:
        c.execute("rollback")
      except:
        pass

  PD_update_button.on_click(on_PD_update_button_clicked)

  def on_PD_reset_button_clicked(b):
    # Reset to original values from database
    setup_personal_details()
    PD_status_msg.value = "Form has been reset."

  PD_reset_button.on_click(on_PD_reset_button_clicked)

  def on_PD_back_button_clicked(b):
    # Update welcome message before going back to Member page
    if current_member['username']:
      update_welcome_message(current_member['username'])
    showPage("Member")

  PD_back_button.on_click(on_PD_back_button_clicked)

  # Function to load user details when entering the page
  def setup_personal_details():
    try:
      # Use the stored username from login
      username = current_member['username']
      if not username:
        username = login_textbox.value  # Fallback

      # Query member details from database
      c.execute("""
        SELECT M_ID, M_USERNAME, FNAME, LNAME, M_EMAIL, M_ADDRESS, M_SEC_Q, M_SEC_A
        FROM MEMBER
        WHERE M_USERNAME = :username
      """, {'username': username})

      result = c.fetchone()
      if result:
        # Update the current_member variable
        current_member['id'] = result[0]
        current_member['username'] = result[1]
        current_member['fname'] = result[2]
        current_member['lname'] = result[3]
        current_member['email'] = result[4]
        current_member['address'] = result[5]
        current_member['sec_q'] = result[6]
        current_member['sec_a'] = result[7]

        # Update the form fields
        PD_id_textbox.value = str(current_member['id'])
        PD_username_textbox.value = current_member['username']
        PD_fname_textbox.value = current_member['fname']
        PD_lname_textbox.value = current_member['lname']
        PD_email_textbox.value = current_member['email']
        PD_address_textbox.value = current_member['address']
        PD_sec_q_dropdown.value = current_member['sec_q']
        PD_sec_a_textbox.value = current_member['sec_a']

        # Also update the welcome message
        update_welcome_message(current_member['username'])

        PD_status_msg.value = ""
      else:
        PD_status_msg.value = "Error loading member details."
        showPage("Introduction")  # Return to login if no details found
    except Exception as e:
      PD_status_msg.value = f"Error: {str(e)}"
      print(f"Error in setup_personal_details: {e}")  # Debug message

  # Display the components
  PD_header = widgets.VBox([PD_title_label, PD_subtitle_label, PD_instructions])
  PD_line_spacer = widgets.HBox([PD_spacer])

  PD_labels = widgets.VBox([
    PD_id_label, PD_username_label, PD_fname_label, PD_lname_label,
    PD_email_label, PD_address_label, PD_sec_q_label, PD_sec_a_label
  ])

  # Create a separate row for username with the notice
  username_row = widgets.HBox([PD_username_textbox, PD_username_notice])

  PD_inputs = widgets.VBox([
    PD_id_textbox, username_row, PD_fname_textbox, PD_lname_textbox,
    PD_email_textbox, PD_address_textbox, PD_sec_q_dropdown, PD_sec_a_textbox
  ])

  PD_form = widgets.HBox([PD_labels, PD_inputs])
  PD_buttons = widgets.HBox([PD_update_button, PD_reset_button, PD_back_button])

  display(widgets.VBox([PD_header, PD_line_spacer, PD_form, PD_status_msg, PD_buttons]))

################ Personal Detail- End ################
################ Member - End ################

################ Message Page ################

with tb_all.output_to('Message'):

  # Page title
  message_title = Label("System Message")
  message_title.style = {'font_weight': 'bold', 'font_size': '18px'}

  # Message content
  message_label = Label("")
  message_label.style = {'font_weight': 'bold', 'font_size': '16px'}

  # Success icon (text-based for simplicity)
  message_icon = Label("✓")
  message_icon.style = {'font_size': '32px', 'color': '#4CAF50'}

  # Back button with description that will change depending on context
  message_back_button = widgets.Button(
    description="Back to Menu",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(message_back_button, SECONDARY_COLOR)

  # Create a context variable to track where to return
  message_context = {'return_to_login': False, 'return_to_member': False}

  def on_message_back_button_clicked(b):
    if message_context['return_to_login']:
      # If we need to return to login (after password reset or registration)
      message_context['return_to_login'] = False
      message_back_button.description = "Back to Menu"
      showPage("Introduction")
    elif message_context['return_to_member']:
      # Return to Member page after order confirmation
      message_context['return_to_member'] = False
      message_back_button.description = "Back to Menu"
      showPage("Member")
    else:
      # Otherwise, return to Member page
      showPage("Member")

  message_back_button.on_click(on_message_back_button_clicked)

  # Layout with centered elements and better spacing
  icon_box = widgets.HBox([message_icon])
  icon_box.layout.justify_content = 'center'

  title_box = widgets.HBox([message_title])
  title_box.layout.justify_content = 'center'

  message_box = widgets.HBox([message_label])
  message_box.layout.justify_content = 'center'

  button_box = widgets.HBox([message_back_button])
  button_box.layout.justify_content = 'center'

  display(widgets.VBox([
    widgets.HTML("<br>"),
    icon_box,
    title_box,
    widgets.HTML("<hr>"),
    message_box,
    widgets.HTML("<br>"),  # Add spacing before button
    button_box
  ]))


##########################################################
################ Shop Products - Begin ######################
##########################################################

with tb_all.output_to('Shop Products'):
  # Shop Products page title
  shop_title = create_header("Browse Our Products")
  shop_subtitle = create_subheader("View available products")

  # Search section
  search_label = Label("Search: ")
  search_textbox = Text(
    value='',
    placeholder='Enter keyword (name, manufacturer, etc.)',
    disabled=False,
    layout=widgets.Layout(width='350px')
  )

  search_button = widgets.Button(
    description="Search",
    layout=widgets.Layout(width='100px', height='30px')
  )

  show_all_button = widgets.Button(
    description="Clear",
    layout=widgets.Layout(width='100px', height='30px')
  )

  # Navigation buttons
  shop_cart_button = widgets.Button(
    description="View Shopping Cart",
    layout=widgets.Layout(width='150px', height='30px')
  )

  shop_back_button = widgets.Button(
    description="Back to Menu",
    layout=widgets.Layout(width='150px', height='30px')
  )

  # Pagination controls
  product_prev_button = widgets.Button(
    description="Previous 5",
    disabled=True,
    layout=widgets.Layout(width='120px', height='30px'),
    style=widgets.ButtonStyle(button_color='#2196F3')  # Blue button
  )

  product_next_button = widgets.Button(
    description="Next 5",
    disabled=True,
    layout=widgets.Layout(width='120px', height='30px'),
    style=widgets.ButtonStyle(button_color='#2196F3')  # Blue button
  )

  # Spacer and status message
  product_spacer = widgets.HTML("<hr>")
  current_page_index = widgets.Label("0")  # Hidden label to track pagination
  shop_status = widgets.Label("", style={'font_weight': 'bold'}, layout=widgets.Layout(padding='10px 0px', margin='10px 0', min_height='40px', width='100%'))

  # Create lists for product data rows
  product_id_textboxes = [Text(value='', description='ID:', disabled=True) for i in range(5)]
  product_name_textboxes = [Text(value='', description='Name:', disabled=True, layout=widgets.Layout(width='300px')) for i in range(5)]
  product_price_textboxes = [Text(value='', description='Price: $', disabled=True) for i in range(5)]
  product_detail_buttons = [widgets.Button(
    description="View Details",
    disabled=True,
    layout=widgets.Layout(width='120px', height='30px'),
    style=widgets.ButtonStyle(button_color='#4CAF50') # Green button
  ) for i in range(5)]


  product_data_HBoxes = [
      widgets.HBox([
          product_id_textboxes[i],
          product_name_textboxes[i],
          product_price_textboxes[i],
          product_detail_buttons[i]
      ]) for i in range(5)
  ]

  # Global variables
  current_products = []
  search_keyword = ""

  # Function to load products with pagination
  def load_products(from_index=1, to_index=5, keyword=""):
    global current_products, search_keyword
    search_keyword = keyword

    try:
      # Construct SQL query based on whether a search term is provided
      if keyword:
        search_param = f"%{keyword}%"
        c.execute("""
          SELECT COUNT(*)
          FROM PRODUCT
          WHERE (UPPER(P_NAME) LIKE UPPER(:keyword) OR
                 UPPER(P_DESCRIPTION) LIKE UPPER(:keyword) OR
                 UPPER(P_MANUFACTURER) LIKE UPPER(:keyword) OR
                 UPPER(P_COLOUR) LIKE UPPER(:keyword))
                AND P_STATUS = 'Active'
                AND P_INVENTORY > 0
        """, {'keyword': search_param})
      else:
        c.execute("""
          SELECT COUNT(*)
          FROM PRODUCT
          WHERE P_STATUS = 'Active' AND P_INVENTORY > 0
        """)

      # Get total record count
      max_record_count = c.fetchone()[0]

      if max_record_count == 0:
        shop_status.value = "No products found matching your criteria."

        # Clear all rows
        for i in range(5):
          product_id_textboxes[i].value = ""
          product_name_textboxes[i].value = ""
          product_price_textboxes[i].value = ""
          product_detail_buttons[i].disabled = True

        # Disable pagination
        product_prev_button.disabled = True
        product_next_button.disabled = True
        return

      # Fetch products for the current page
      if keyword:
        search_param = f"%{keyword}%"
        c.execute("""
          SELECT P_ID, P_NAME, P_DESCRIPTION, P_PRICE, P_WEIGHT, P_COLOUR,
                 P_CAPACITY, P_MANUFACTURER, P_STATUS, P_INVENTORY,
                 ROW_NUMBER() OVER (ORDER BY P_ID ASC) as row_num
          FROM PRODUCT
          WHERE (UPPER(P_NAME) LIKE UPPER(:keyword) OR
                 UPPER(P_DESCRIPTION) LIKE UPPER(:keyword) OR
                 UPPER(P_MANUFACTURER) LIKE UPPER(:keyword) OR
                 UPPER(P_COLOUR) LIKE UPPER(:keyword))
                AND P_STATUS = 'Active'
                AND P_INVENTORY > 0
          ORDER BY P_ID ASC
        """, {'keyword': search_param})
      else:
        c.execute("""
          SELECT P_ID, P_NAME, P_DESCRIPTION, P_PRICE, P_WEIGHT, P_COLOUR,
                 P_CAPACITY, P_MANUFACTURER, P_STATUS, P_INVENTORY,
                 ROW_NUMBER() OVER (ORDER BY P_ID ASC) as row_num
          FROM PRODUCT
          WHERE P_STATUS = 'Active' AND P_INVENTORY > 0
          ORDER BY P_ID ASC
        """)

      products = c.fetchall()
      current_products = products

      # Display products in the UI
      i = 0
      for product in products:
        row_num = product[10]  # ROW_NUMBER from SQL query
        if from_index <= row_num <= to_index:
          product_id_textboxes[i].value = str(product[0])  # P_ID
          product_name_textboxes[i].value = str(product[1])  # P_NAME
          product_price_textboxes[i].value = str(product[3])  # P_PRICE
          product_detail_buttons[i].disabled = False
          i += 1

      # Clear any remaining rows
      for j in range(i, 5):
        product_id_textboxes[j].value = ""
        product_name_textboxes[j].value = ""
        product_price_textboxes[j].value = ""
        product_detail_buttons[j].disabled = True

      # Update pagination controls
      current_page_index.value = str(from_index)

      # Update navigation buttons
      product_prev_button.disabled = (from_index <= 1)
      product_next_button.disabled = (max_record_count <= to_index)

      if keyword:
        shop_status.value = f"Search results for '{keyword}': Showing {from_index} to {min(to_index, max_record_count)} of {max_record_count} products"
      else:
        shop_status.value = f"Showing {from_index} to {min(to_index, max_record_count)} of {max_record_count} products"

    except Exception as e:
      shop_status.value = f"Error loading products: {str(e)}"

  # Button Handlers
  def on_search_button_clicked(b):
    keyword = search_textbox.value.strip()
    # Reset to first page when searching
    clear_product_display()
    load_products(1, 5, keyword)

  search_button.on_click(on_search_button_clicked)

  def on_show_all_button_clicked(b):
    search_textbox.value = ""
    clear_product_display()
    load_products(1, 5, "")

  show_all_button.on_click(on_show_all_button_clicked)

  def on_product_prev_button_clicked(b):
    from_index = int(current_page_index.value) - 5
    to_index = from_index + 4
    clear_product_display()
    load_products(from_index, to_index, search_keyword)

  product_prev_button.on_click(on_product_prev_button_clicked)

  def on_product_next_button_clicked(b):
    from_index = int(current_page_index.value) + 5
    to_index = from_index + 4
    clear_product_display()
    load_products(from_index, to_index, search_keyword)

  product_next_button.on_click(on_product_next_button_clicked)

  def on_shop_back_button_clicked(b):
    showPage("Member")

  shop_back_button.on_click(on_shop_back_button_clicked)

  def on_shop_cart_button_clicked(b):
    setup_shopping_cart()
    showPage("Shopping Cart")

  shop_cart_button.on_click(on_shop_cart_button_clicked)

  def clear_product_display():
    # Clear all product rows -
    for i in range(5):
      product_id_textboxes[i].value = ""
      product_name_textboxes[i].value = ""
      product_price_textboxes[i].value = ""
      product_detail_buttons[i].disabled = True

    # Reset navigation
    product_prev_button.disabled = True
    product_next_button.disabled = True
    shop_status.value = ""

  def on_product_detail_button_clicked(b):
    # Find which button was clicked
    button_num = 0
    for button_num in range(len(product_detail_buttons)):
      if product_detail_buttons[button_num] == b:
        product_id_selected = product_id_textboxes[button_num].value
        break

    # Navigate to product detail page
    if product_id_selected:
      show_product_details(product_id_selected)
    else:
      shop_status.value = "Error: Cannot view details for empty product."

  # Assign the event handler to all detail buttons
  for detail_btn in product_detail_buttons:
    detail_btn.on_click(on_product_detail_button_clicked)

  # Layout the page
  header_box = widgets.VBox([
    shop_title,
    shop_subtitle
  ])

  search_box = widgets.HBox([
    search_label,
    search_textbox,
    search_button,
    show_all_button
  ], layout=widgets.Layout(padding='10px 0px'))

  product_rows = widgets.VBox([
    product_data_HBoxes[i] for i in range(5)
  ])

  pagination_box = widgets.HBox([
    product_prev_button,
    product_next_button,
    current_page_index
  ], layout=widgets.Layout(padding='10px 0px'))

  # Hide the current_page_index (used for internal tracking)
  current_page_index.layout.display = 'none'

  navigation_box = widgets.HBox([
    shop_cart_button,
    shop_back_button
  ], layout=widgets.Layout(padding='10px 0px'))

  # Display all components
  display(widgets.VBox([
    header_box,
    search_box,
    widgets.HTML("<hr>"),
    widgets.HTML("<div style='height: 5px;'></div>"),  # Add a small spacer
    shop_status,
    widgets.HTML("<div style='height: 5px;'></div>"),  # Add a small spacer
    product_rows,
    widgets.HTML("<hr>"),
    pagination_box,
    navigation_box
  ]))

  # Initialize product display
  load_products(1, 5, "")

################ Shop Products - End ######################

##########################################################
################ Product Details - Begin #################
##########################################################

with tb_all.output_to('Product Details'):
  # Product detail page elements with consistent styling
  product_detail_title = create_header("Product Details")
  product_detail_subtitle = create_subheader("View product information below")

  # Create styled output area for product details
  product_detail_output = widgets.Output(layout={'border': '1px solid #e0e0e0', 'padding': '10px'})

  # Status message area
  product_detail_status = create_styled_message("", "info")

  # Navigation buttons
  product_detail_back_btn = widgets.Button(
    description="Back to Products",
    layout=ACTION_BUTTON_LAYOUT
  )
  # Make Product Details back button bold
  product_detail_back_btn.style = {'font_weight': 'bold'}

  product_detail_cart_btn = widgets.Button(
    description="View Cart",
    layout=ACTION_BUTTON_LAYOUT
  )
  # Make Product Details cart button bold
  product_detail_cart_btn.style = {'font_weight': 'bold'}

  # Create layout with consistent spacing
  display(widgets.VBox([
      product_detail_title,
      product_detail_subtitle,
      SEPARATOR,
      product_detail_output,
      SECTION_SPACING,
      product_detail_status,
      widgets.HBox([product_detail_back_btn, product_detail_cart_btn]),
      SEPARATOR
  ]))

  # Button handlers
  def on_product_detail_back_btn_clicked(b):
    showPage("Shop Products")

  product_detail_back_btn.on_click(on_product_detail_back_btn_clicked)

  def on_product_detail_cart_btn_clicked(b):
    setup_shopping_cart()
    showPage("Shopping Cart")

  product_detail_cart_btn.on_click(on_product_detail_cart_btn_clicked)

# Update the show_product_details function to use the Product Details tab
def show_product_details(product_id):
  with product_detail_output:
    product_detail_output.clear_output()

    try:
      c.execute("""
        SELECT P_ID, P_NAME, P_DESCRIPTION, P_PRICE, P_WEIGHT, P_COLOUR,
              P_CAPACITY, P_MANUFACTURER, P_STATUS, P_INVENTORY
        FROM PRODUCT
        WHERE P_ID = :p_id AND P_STATUS = 'Active'
      """, {'p_id': product_id})

      product = c.fetchone()
      if not product:
        display(widgets.HTML("<p>Product not found or unavailable.</p>"))
        return

      p_id, p_name, p_description, p_price, p_weight, p_color, p_capacity, p_manufacturer, p_status, p_inventory = product

      # Create HTML content with consistent styling
      html_content = f"""
      <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
          <div style="background-color: #f5f5f5; padding: 10px; text-align: center;">
              <h2 style="margin: 0;">PRODUCT DETAILS</h2>
          </div>

          <div style="margin: 20px 0;">
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Product ID:</div>
                  <div>{p_id}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Name:</div>
                  <div>{p_name}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Price:</div>
                  <div>${p_price}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Manufacturer:</div>
                  <div>{p_manufacturer}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Color:</div>
                  <div>{p_color}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Capacity:</div>
                  <div>{p_capacity}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Weight:</div>
                  <div>{p_weight}</div>
              </div>
              <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                  <div style="font-weight: bold;">Availability:</div>
                  <div>{p_inventory} in stock</div>
              </div>
          </div>

          <div style="margin: 20px 0;">
              <h3 style="border-bottom: 1px solid #ddd; padding-bottom: 5px;">DESCRIPTION</h3>
              <p style="line-height: 1.5;">{p_description}</p>
          </div>
      </div>
      """

      # Display the HTML content
      display(widgets.HTML(html_content))

      # Create quantity selector and add to cart button
      qty_label = widgets.Label("Select Quantity:")

      # Set options based on inventory status
      if p_inventory > 0:
        qty_dropdown = widgets.Dropdown(
          options=list(range(1, p_inventory + 1)),
          value=1,
          description="Qty:",
          layout=widgets.Layout(width='150px'),
          disabled=False
        )
      else:
        # Create a disabled dropdown with just option 1 when out of stock
        qty_dropdown = widgets.Dropdown(
          options=[1],
          value=1,
          description="Qty:",
          layout=widgets.Layout(width='150px'),
          disabled=True
        )

      add_cart_btn = widgets.Button(
        description="Add to Cart",
        layout=widgets.Layout(width='150px'),
        style=widgets.ButtonStyle(button_color=PRIMARY_COLOR),
        disabled=(p_inventory <= 0),   # Disable button if out of stock
      )

      # Function to add product to cart
      def add_to_cart(b):
        try:
          # First check if we have a valid member ID
          if not current_member['username']:
            product_detail_status.value = "Please log in before adding items to your cart."
            return

          # Make sure we have the member ID
          member_id = None
          if current_member['id']:
            member_id = current_member['id']
          else:
            # Try to get the ID using the username
            c.execute("SELECT M_ID FROM MEMBER WHERE M_USERNAME = :username",
                     {'username': current_member['username']})
            result = c.fetchone()
            if result:
              member_id = result[0]
              current_member['id'] = member_id
            else:
              product_detail_status.value = "Error retrieving your account information. Please log in again."
              return

          # Proceed with adding to cart only if we have a valid member ID
          if not member_id:
            product_detail_status.value = "Please log in before adding items to your cart."
            return

          quantity = qty_dropdown.value

          # Check if this product is already in the cart
          c.execute("""
            SELECT SCI_ID, SCI_QTY FROM SHOPPING_CART_ITEM
            WHERE MEMBER_M_ID = :member_id AND PRODUCT_P_ID = :product_id
          """, {'member_id': member_id, 'product_id': p_id})

          cart_item = c.fetchone()

          if cart_item:
            # Update existing cart item
            sci_id, current_qty = cart_item
            new_qty = current_qty + quantity

            # Update the cart item quantity (removed inventory check)
            c.execute("""
              UPDATE SHOPPING_CART_ITEM
              SET SCI_QTY = :new_qty
              WHERE SCI_ID = :sci_id
            """, {'new_qty': new_qty, 'sci_id': sci_id})

            product_detail_status.value = f"{quantity} more units of {p_name} added to your cart."
          else:
            # Create a new cart item
            c.execute("SELECT MAX(SCI_ID) FROM SHOPPING_CART_ITEM")
            result = c.fetchone()
            new_sci_id = 1 if result[0] is None else result[0] + 1

            c.execute("""
              INSERT INTO SHOPPING_CART_ITEM (SCI_ID, SCI_QTY, MEMBER_M_ID, PRODUCT_P_ID)
              VALUES (:sci_id, :sci_qty, :member_id, :product_id)
            """, {
              'sci_id': new_sci_id,
              'sci_qty': quantity,
              'member_id': member_id,
              'product_id': p_id
            })

            product_detail_status.value = f"{p_name} added to your cart."

          c.execute("commit")
        except Exception as e:
          product_detail_status.value = f"Error adding to cart: {str(e)}"
          try:
            c.execute("rollback")
          except:
            pass

      add_cart_btn.on_click(add_to_cart)

      # Display quantity selector and add button
      display(widgets.HBox([qty_label, qty_dropdown, add_cart_btn]))

      # Add "Out of Stock" message if inventory is 0
      if p_inventory <= 0:
        out_of_stock_label = widgets.HTML("<span style='font-weight: bold;'>Out of Stock</span>")
        display(out_of_stock_label)

    except Exception as e:
      display(widgets.HTML(f"<p>Error displaying product details: {str(e)}</p>"))

  # Switch to the Product Details tab
  showPage("Product Details")

##########################################################
################ Shopping Cart - Begin ####################
##########################################################

with tb_all.output_to('Shopping Cart'):
  # Shopping Cart page
  cart_title = create_header("Your Shopping Cart")
  cart_subtitle = create_subheader("View and manage items in your cart")
  cart_status = Label("")
  cart_status.style = {'font_weight': 'bold'}

  # Cart display area
  cart_output = widgets.Output(layout={'border': '1px solid #e0e0e0', 'padding': '10px', 'margin': '10px 0'})

  # Order summary section
  summary_output = widgets.Output(layout={'border': '1px solid #e0e0e0', 'padding': '10px', 'margin': '10px 0', 'background-color': '#f9f9f9'})

  # Navigation buttons
  continue_shopping_btn = widgets.Button(
    description="Continue Shopping",
    layout=ACTION_BUTTON_LAYOUT
  )
  style_button(continue_shopping_btn, SECONDARY_COLOR)

  checkout_btn = widgets.Button(
    description="Proceed to Checkout",
    layout=ACTION_BUTTON_LAYOUT
  )
  style_button(checkout_btn, PRIMARY_COLOR)

  cart_back_btn = widgets.Button(
    description="Back to Menu",
    layout=ACTION_BUTTON_LAYOUT
  )
  style_button(cart_back_btn, NEUTRAL_COLOR)

  # Global variables for cart data
  cart_items = []
  cart_total = 0

  # Function to ensure member ID is available
  def ensure_member_id():
    """
    Ensures that the current_member dictionary has a valid ID.
    If username exists but ID is missing, retrieves the ID from the database.
    Returns True if member ID is available, False otherwise.
    """
    # If ID already exists and is not empty, we're good
    if current_member['id']:
      return True

    # If username exists but ID is missing, try to fetch ID from database
    if current_member['username']:
      try:
        c.execute("""
          SELECT M_ID FROM MEMBER
          WHERE M_USERNAME = :username
        """, {'username': current_member['username']})
        result = c.fetchone()
        if result:
          # Store the ID in the current_member dictionary
          current_member['id'] = result[0]
          print(f"Retrieved member ID: {current_member['id']} for user {current_member['username']}")
          return True
      except Exception as e:
        print(f"Error retrieving member ID: {e}")

    # If we couldn't get an ID
    return False

  # Add a function to log in the user through their username alone (for testing)
  def login_by_username(username):
    """
    Helper function to log in a user by username only.
    Retrieves all necessary member information and updates current_member.
    For testing purposes.
    """
    try:
      c.execute("""
        SELECT M_ID, M_USERNAME, FNAME, LNAME, M_EMAIL, M_ADDRESS, M_SEC_Q, M_SEC_A
        FROM MEMBER
        WHERE M_USERNAME = :username
      """, {'username': username})

      result = c.fetchone()
      if result:
        # Update the current_member variable
        current_member['id'] = result[0]
        current_member['username'] = result[1]
        current_member['fname'] = result[2]
        current_member['lname'] = result[3]
        current_member['email'] = result[4]
        current_member['address'] = result[5]
        current_member['sec_q'] = result[6]
        current_member['sec_a'] = result[7]

        print(f"Logged in as {username} with ID {current_member['id']}")
        return True
      else:
        print(f"Username '{username}' not found")
        return False
    except Exception as e:
      print(f"Error logging in by username: {e}")
      return False

  # Get member ID following the pattern in setup_personal_details
  def get_member_id_for_cart():
    """
    Gets the member ID using the same approach as in setup_personal_details.
    Returns the member ID or None if not found.
    """
    try:
      # Use the stored username from login
      username = current_member['username']
      if not username:
        return None

      # Query member ID from database
      c.execute("""
        SELECT M_ID FROM MEMBER
        WHERE M_USERNAME = :username
      """, {'username': username})

      result = c.fetchone()
      if result:
        # Update the current_member variable
        current_member['id'] = result[0]
        return result[0]
      else:
        return None
    except Exception as e:
      cart_status.value = f"Error retrieving member information: {str(e)}"
      return None

  # Clean implementation of add_to_cart
  def add_to_cart(product_id, quantity):
    """
    Adds a product to the shopping cart.
    Uses the same pattern as personal details for member ID retrieval.
    """
    try:
      # Get member ID using the pattern from setup_personal_details
      member_id = None

      # If we already have the ID, use it
      if current_member['id']:
        member_id = current_member['id']
      else:
        # Otherwise get it from the database
        member_id = get_member_id_for_cart()

      # Verify we have the ID
      if not member_id:
        cart_status.value = "Please log in to add items to your cart."
        return False

      # Check if product exists and is available
      c.execute("""
        SELECT P_ID, P_NAME, P_INVENTORY, P_PRICE
        FROM PRODUCT
        WHERE P_ID = :product_id
        AND P_STATUS = 'Active'
        AND P_INVENTORY > 0
      """, {'product_id': product_id})

      product = c.fetchone()
      if not product:
        cart_status.value = "Product is not available."
        return False

      p_id, p_name, inventory, price = product

      # Check if quantity is valid
      if quantity <= 0:
        cart_status.value = "Please select a valid quantity."
        return False

      # Check if product already exists in cart
      c.execute("""
        SELECT SCI_ID, SCI_QTY
        FROM SHOPPING_CART_ITEM
        WHERE MEMBER_M_ID = :member_id
        AND PRODUCT_P_ID = :product_id
      """, {'member_id': member_id, 'product_id': p_id})

      cart_item = c.fetchone()

      if cart_item:
        # Update existing cart item
        sci_id, current_qty = cart_item
        new_qty = current_qty + quantity

        # Update the cart item quantity (removed inventory check)
        c.execute("""
          UPDATE SHOPPING_CART_ITEM
          SET SCI_QTY = :new_qty
          WHERE SCI_ID = :sci_id
        """, {'new_qty': new_qty, 'sci_id': sci_id})

        cart_status.value = f"{quantity} more units of {p_name} added to your cart."
      else:
        # Create a new cart item
        c.execute("SELECT MAX(SCI_ID) FROM SHOPPING_CART_ITEM")
        result = c.fetchone()
        new_sci_id = 1 if result[0] is None else result[0] + 1

        # Insert new item
        c.execute("""
          INSERT INTO SHOPPING_CART_ITEM (SCI_ID, SCI_QTY, MEMBER_M_ID, PRODUCT_P_ID)
          VALUES (:sci_id, :sci_qty, :member_id, :product_id)
        """, {
          'sci_id': new_sci_id,
          'sci_qty': quantity,
          'member_id': member_id,
          'product_id': p_id
        })

        cart_status.value = f"{p_name} added to your cart."

      # Commit changes
      c.execute("commit")
      return True

    except Exception as e:
      cart_status.value = f"Error adding to cart: {str(e)}"
      try:
        c.execute("rollback")
      except:
        pass
      return False

  # Add the update_cart_item function
  def update_cart_item(sci_id, new_qty):
    """
    Updates the quantity of an item in the shopping cart, or removes it if quantity is 0.
    Returns True if the update was successful, False otherwise.
    """
    try:
      if new_qty <= 0:
        # Delete the item if quantity is 0
        c.execute("""
          DELETE FROM SHOPPING_CART_ITEM
          WHERE SCI_ID = :sci_id
        """, {'sci_id': sci_id})
        cart_status.value = "Item removed from cart."
      else:
        # Get product info for confirmation message
        c.execute("""
          SELECT p.P_NAME
          FROM SHOPPING_CART_ITEM sci
          JOIN PRODUCT p ON sci.PRODUCT_P_ID = p.P_ID
          WHERE sci.SCI_ID = :sci_id
        """, {'sci_id': sci_id})

        result = c.fetchone()
        if result:
          p_name = result[0]

          # Update quantity without inventory check
          c.execute("""
            UPDATE SHOPPING_CART_ITEM
            SET SCI_QTY = :new_qty
            WHERE SCI_ID = :sci_id
          """, {'sci_id': sci_id, 'new_qty': new_qty})

          cart_status.value = f"Updated quantity for {p_name}."
        else:
          cart_status.value = "Error: Item not found in cart."
          return False

      c.execute("commit")
      # Refresh cart items and total after update
      load_cart_items()
      return True
    except Exception as e:
      cart_status.value = f"Error updating cart: {str(e)}"
      try:
        c.execute("rollback")
      except:
        pass
      return False

  # Add the missing load_cart_items function
  def load_cart_items():
    global cart_items, cart_total
    try:
      # Get member ID using the pattern from setup_personal_details
      member_id = None

      # If we already have the ID, use it
      if current_member['id']:
        member_id = current_member['id']
      else:
        # Otherwise get it from the database
        member_id = get_member_id_for_cart()

      # Verify we have the ID
      if not member_id:
        cart_status.value = "Please log in to view your cart."
        cart_total = 0
        checkout_btn.disabled = True
        return []

      c.execute("""
        SELECT sci.SCI_ID, sci.SCI_QTY, p.P_ID, p.P_NAME, p.P_PRICE, p.P_INVENTORY
        FROM SHOPPING_CART_ITEM sci
        JOIN PRODUCT p ON sci.PRODUCT_P_ID = p.P_ID
        WHERE sci.MEMBER_M_ID = :member_id
        AND p.P_STATUS = 'Active'
        AND p.P_INVENTORY > 0
        ORDER BY sci.SCI_ID
      """, {'member_id': member_id})

      cart_items = c.fetchall()

      # Calculate total
      cart_total = sum(float(item[4]) * item[1] for item in cart_items)

      # Disable checkout button if cart is empty or total is zero
      if not cart_items or cart_total <= 0:
        checkout_btn.disabled = True
      else:
        checkout_btn.disabled = False

      return cart_items
    except Exception as e:
      cart_status.value = f"Error loading cart: {str(e)}"
      cart_total = 0
      checkout_btn.disabled = True
      return []

  # Function to display cart items and summary
  def display_cart():
    items = load_cart_items()

    with cart_output:
      cart_output.clear_output()

      if not items:
        display(widgets.HTML("<div style='padding: 15px; text-align: center; font-size: 16px;'>Your shopping cart is empty.</div>"))
        # Clear summary when cart is empty
        with summary_output:
          summary_output.clear_output()
        checkout_btn.disabled = True
        return
      else:
        checkout_btn.disabled = False

      # Create a formatted HTML table instead of ASCII lines
      html_content = f"""
      <div style="width: 100%; overflow-x: auto;">
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
          <thead>
            <tr style="background-color: {NEUTRAL_COLOR}; border-bottom: 2px solid #ddd;">
              <th style="padding: 10px; text-align: left; width: 40%;">Item</th>
              <th style="padding: 10px; text-align: right; width: 20%;">Price</th>
              <th style="padding: 10px; text-align: right; width: 20%;">Quantity</th>
              <th style="padding: 10px; text-align: right; width: 20%;">Subtotal</th>
            </tr>
          </thead>
          <tbody>
      """

      # Display each cart item with its details
      for item in items:
        sci_id, qty, p_id, name, price, inventory = item
        subtotal = float(price) * qty

        print(f"{name:<30} ${price:<9} {qty:<10} ${subtotal:<9.2f}")

        # Create a horizontal line to visually separate the item from its controls
        print(f"{'-' * 70}")

        # Create a horizontal line to visually separate the item from its controls
        print(f"{'-' * 70}")

        # Create a horizontal layout with quantity controls and update/remove buttons
        qty_label = widgets.Label("Change quantity:")
        qty_dropdown = widgets.Dropdown(
          options=list(range(0, max(inventory, qty) + 1)),  # Include 0 for removal
          value=qty,
          description="Qty:",
          layout=widgets.Layout(width='180px')
        )

        # Create update and remove buttons with proper styling
        update_btn = widgets.Button(
          description="Update",
          layout=widgets.Layout(width='130px', height='30px')
        )
        style_button(update_btn, SECONDARY_COLOR)

        remove_btn = widgets.Button(
          description="Remove",
          button_style='danger',
          layout=widgets.Layout(width='130px', height='30px')
        )
        style_button(remove_btn, '#FF5252')

        # Create handlers for the buttons
        def create_update_handler(item_id, dropdown):
          def update_item(b):
            if update_cart_item(item_id, dropdown.value):
              # Check if this was the last item in the cart
              c.execute("""
                SELECT COUNT(*) FROM SHOPPING_CART_ITEM
                WHERE MEMBER_M_ID = :member_id
              """, {'member_id': current_member['id']})
              count = c.fetchone()[0]

              if count == 0:
                # If cart is now empty, clear the summary and disable checkout
                with summary_output:
                  summary_output.clear_output()
                  display(widgets.HTML("<div style='padding: 15px; text-align: center; font-size: 16px;'>Your shopping cart is empty.</div>"))
                checkout_btn.disabled = True

              display_cart()  # Refresh display if update was successful
          return update_item

        def create_remove_handler(item_id):
          def remove_item(b):
            if update_cart_item(item_id, 0):  # Setting quantity to 0 removes the item
              display_cart()
          return remove_item

        # Attach handlers to buttons
        update_btn.on_click(create_update_handler(sci_id, qty_dropdown))
        remove_btn.on_click(create_remove_handler(sci_id))

        # Enhance the dropdown appearance and make it more intuitive
        qty_dropdown.description = "Select: "  # More clear description
        qty_dropdown.layout.width = '180px'  # Wider dropdown

        # Add a helper text above the controls
        qty_helper = widgets.HTML(f"<div style='margin-bottom:5px; color:#555;'><b>Current quantity:</b> {qty} ⟹ Change using dropdown</div>")

        # Create spacers for better layout
        spacer1 = widgets.HTML("&nbsp;&nbsp;&nbsp;&nbsp;")  # Space after dropdown
        spacer2 = widgets.HTML("&nbsp;&nbsp;&nbsp;&nbsp;")  # Space between buttons

        # Put everything in a single row: helper text on top, then dropdown and buttons in one row
        controls = widgets.VBox([
          qty_helper,
          widgets.HBox([qty_dropdown, spacer1, update_btn, spacer2, remove_btn])
        ])

        # Set layout properties for the controls row
        controls.layout.align_items = 'center'
        controls.layout.margin = '5px 0'

        # Display the controls
        display(controls)

        # Add a separator between items (not for the last item)
        if item != items[-1]:
          display(widgets.HTML(f"<div style='height: 1px; background-color: {NEUTRAL_COLOR}; margin: 10px 0;'></div>"))

    # Show order summary in a separate output area
    with summary_output:
      summary_output.clear_output()

      if not items:
        # Display empty cart message in summary
        print("Your shopping cart is empty.")
        return

      # Create a visually distinct order summary
      print(f"Order Summary")
      print(f"{'-' * 30}")
      print(f"Total Items: {sum(item[1] for item in items)}")
      print(f"Total Price: ${cart_total:.2f}")

      # Add checkout instructions
      if cart_total > 0:
        print("\nReady to complete your purchase?")
        print("Click 'Proceed to Checkout' below.")
      else:
        checkout_btn.disabled = True

      # Remove these lines that reference html_summary
      # html_summary += "</div>"
      # display(widgets.HTML(html_summary))

  # Navigation buttons with improved width to ensure text is fully displayed
  continue_shopping_btn = widgets.Button(
    description="Continue Shopping",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(continue_shopping_btn, SECONDARY_COLOR)

  checkout_btn = widgets.Button(
    description="Proceed to Checkout",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(checkout_btn, PRIMARY_COLOR)

  cart_back_btn = widgets.Button(
    description="Back to Menu",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(cart_back_btn, NEUTRAL_COLOR)

  # Update setup_shopping_cart
  def setup_shopping_cart():
    # Check if user is logged in
    if not current_member['username']:
      with cart_output:
        cart_output.clear_output()
        print("Please log in to view your shopping cart.")

      # Clear summary output as well
      with summary_output:
        summary_output.clear_output()

      # Disable checkout button
      checkout_btn.disabled = True
      cart_status.value = "Please log in to view your shopping cart."
      return

    # Make sure we have a member ID
    if not current_member['id']:
      member_id = get_member_id_for_cart()
      if not member_id:
        with cart_output:
          cart_output.clear_output()
          print("Could not retrieve your member information. Please log in again.")

        # Clear summary output as well
        with summary_output:
          summary_output.clear_output()

        checkout_btn.disabled = True
        return

    # If all is well, enable checkout and display cart
    checkout_btn.disabled = False
    display_cart()

  # Event handlers for buttons
  def on_continue_shopping_btn_clicked(b):
    showPage("Shop Products")

  continue_shopping_btn.on_click(on_continue_shopping_btn_clicked)

  def on_checkout_btn_clicked(b):
    if not cart_items:
      cart_status.value = "Your cart is empty. Please add items before checkout."
      return

    # Check if user is logged in
    if not current_member['id']:
      cart_status.value = "Please log in to proceed to checkout."
      return

    try:
      # Make sure cart data is up to date
      load_cart_items()
      # Display checkout summary
      display_checkout_summary()
      # Navigate to checkout
      showPage("Checkout")
    except Exception as e:
      cart_status.value = f"Error proceeding to checkout: {str(e)}"
      print(f"Error in checkout: {e}")

  checkout_btn.on_click(on_checkout_btn_clicked)

  def on_cart_back_btn_clicked(b):
    showPage("Member")

  cart_back_btn.on_click(on_cart_back_btn_clicked)

  # Layout the page
  header_box = widgets.VBox([
    cart_title,
    cart_subtitle,
    widgets.HTML("<hr>")
  ])

  status_box = widgets.HBox([cart_status], layout=widgets.Layout(
    min_height='30px',
    padding='5px',
    margin='5px 0'
  ))

  navigation_box = widgets.HBox([
    continue_shopping_btn,
    checkout_btn,
    cart_back_btn
  ], layout=widgets.Layout(
    justify_content='space-between',
    margin='10px 0'
  ))

  # Display all components with improved layout
  display(widgets.VBox([
    header_box,
    status_box,
    cart_output,
    SEPARATOR,
    summary_output,
    navigation_box
  ], layout=widgets.Layout(
    padding='10px',
    width='100%'
  )))

################ Shopping Cart - End ######################

##########################################################
################ Checkout - Begin ######################
##########################################################

with tb_all.output_to('Checkout'):
  # Checkout page
  checkout_title = create_header("Checkout")
  checkout_subtitle = create_subheader("Complete your purchase")
  checkout_status = Label("")
  checkout_status.style = {'font_weight': 'bold'}

  # Order summary section with improved styling
  checkout_output = widgets.Output(layout={'border': '1px solid #e0e0e0', 'padding': '10px', 'margin': '10px 0', 'background-color': '#f9f9f9'})

  # Payment information
  payment_section_label = Label("Payment Information")
  payment_section_label.style = {'font_weight': 'bold', 'font_size': '16px'}

  credit_card_label = Label("Credit Card Number:")
  credit_card_textbox = widgets.Text(
    value='',
    placeholder='Enter 16-digit number',
    disabled=False,
    layout=widgets.Layout(width='250px')
  )

  expiry_date_label = Label("Expiry Date (MM/YYYY):")
  expiry_date_textbox = widgets.Text(
    value='',
    placeholder='MM/YYYY',
    disabled=False,
    layout=widgets.Layout(width='250px')
  )

  cvc_label = Label("CVC:")
  cvc_textbox = widgets.Text(
    value='',
    placeholder='3-digit code',
    disabled=False,
    layout=widgets.Layout(width='250px')
  )

  # Trade-in section
  tradein_section_label = Label("Trade-in Service (Optional)")
  tradein_section_label.style = {'font_weight': 'bold', 'font_size': '16px'}

  has_tradein_checkbox = widgets.Checkbox(
    value=False,
    description='I want to trade in device(s)',
    disabled=False
  )

  # Container for trade-in devices
  tradein_devices_container = widgets.VBox([])
  tradein_devices_container.layout.display = 'none'

  # List to store trade-in device widgets
  tradein_devices = []

  # Add trade-in device button
  add_tradein_btn = widgets.Button(
    description="+ Add Another Device",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(add_tradein_btn, SECONDARY_COLOR)
  add_tradein_btn.layout.display = 'none'

  # Function to create a new trade-in device form
  def create_tradein_device_form():
    device_index = len(tradein_devices)

    # Create device description field
    device_label = Label(f"Device #{device_index + 1} Description:")
    device_textbox = widgets.Text(value='', placeholder='e.g. iPhone 12 Pro 256GB', disabled=False)

    # Create serial number field
    serial_label = Label(f"Device #{device_index + 1} Serial Number:")
    serial_textbox = widgets.Text(value='', placeholder='Enter serial number', disabled=False)

    # Create remove button (except for first device)
    if device_index > 0:
      remove_btn = widgets.Button(
        description="Remove",
        button_style='danger',
        layout=widgets.Layout(width='80px')
      )

      # Create handler for remove button
      def on_remove_clicked(b):
        # Find the index of this device in the list
        for i, device in enumerate(tradein_devices):
          if device['remove_btn'] == b:
            # Remove this device from the list
            removed_device = tradein_devices.pop(i)
            # Update the container children
            update_tradein_container()
            break

      remove_btn.on_click(on_remove_clicked)
    else:
      remove_btn = None

    # Create a device entry object
    device_entry = {
      'index': device_index,
      'device_label': device_label,
      'device_textbox': device_textbox,
      'serial_label': serial_label,
      'serial_textbox': serial_textbox,
      'remove_btn': remove_btn
    }

    # Add to the list of devices
    tradein_devices.append(device_entry)

    # Update the container
    update_tradein_container()

    return device_entry

  # Function to update the trade-in container
  def update_tradein_container():
    # Create a list of widgets to display
    container_widgets = []

    for device in tradein_devices:
      # Add device description
      container_widgets.append(widgets.HBox([
        device['device_label'],
        device['device_textbox']
      ]))

      # Add serial number
      container_widgets.append(widgets.HBox([
        device['serial_label'],
        device['serial_textbox']
      ]))

      # Add remove button if it exists
      if device['remove_btn']:
        container_widgets.append(widgets.HBox([device['remove_btn']]))

      # Add a separator
      container_widgets.append(widgets.HTML("<hr style='margin: 5px 0;'>"))

    # Add the add button
    container_widgets.append(widgets.HBox([add_tradein_btn]))

    # Update the container children
    tradein_devices_container.children = container_widgets

  # Function to handle add tradein button
  def on_add_tradein_clicked(b):
    create_tradein_device_form()

  add_tradein_btn.on_click(on_add_tradein_clicked)

  # Function to handle trade-in checkbox
  def on_tradein_checkbox_change(change):
    if change['new']:  # If checkbox is checked
      # Clear any existing devices
      tradein_devices.clear()
      # Create first device form
      create_tradein_device_form()
      # Show container and add button
      tradein_devices_container.layout.display = 'block'
      add_tradein_btn.layout.display = 'block'
    else:
      # Hide container and add button
      tradein_devices_container.layout.display = 'none'
      add_tradein_btn.layout.display = 'none'
      # Clear devices
      tradein_devices.clear()
      update_tradein_container()

  has_tradein_checkbox.observe(on_tradein_checkbox_change, names='value')

  # Function to display order summary
  def display_checkout_summary():
    global cart_items, cart_total

    with checkout_output:
      checkout_output.clear_output()

      if not cart_items:
        print("Your cart is empty. Please add items before checkout.")
        return

      print(f"Order Summary\n{'-' * 50}")
      print(f"{'Item':<30} {'Price':<10} {'Quantity':<10} {'Subtotal':<10}")
      print(f"{'-' * 50}")

      for item in cart_items:
        sci_id, qty, p_id, name, price, inventory = item
        subtotal = float(price) * qty

        print(f"{name:<30} ${price:<9} {qty:<10} ${subtotal:<9}")

      print(f"{'-' * 50}")
      print(f"Total: ${cart_total:.2f}")

  # Function to validate credit card info
  def validate_payment_info():
    # Credit card validation - simple check for 16 digits
    cc_num = credit_card_textbox.value.strip().replace(' ', '')
    if not cc_num.isdigit() or len(cc_num) != 16:
      checkout_status.value = "Please enter a valid 16-digit credit card number."
      return False

    # Expiry date validation (MM/YYYY format)
    expiry = expiry_date_textbox.value.strip()
    if not re.match(r'^(0[1-9]|1[0-2])\/20[2-9][0-9]$', expiry):
      checkout_status.value = "Please enter a valid expiry date (MM/YYYY)."
      return False

    # CVC validation - 3 digits
    cvc = cvc_textbox.value.strip()
    if not cvc.isdigit() or len(cvc) != 3:
      checkout_status.value = "Please enter a valid 3-digit CVC code."
      return False

    # Validate trade-in devices if enabled
    if has_tradein_checkbox.value:
      for device in tradein_devices:
        device_desc = device['device_textbox'].value.strip()
        serial_num = device['serial_textbox'].value.strip()

        if not device_desc:
          checkout_status.value = f"Please enter a description for Device #{device['index'] + 1}."
          return False

        if not serial_num:
          checkout_status.value = f"Please enter a serial number for Device #{device['index'] + 1}."
          return False

    return True

  # Function to complete order
  def place_order():
    global cart_items, cart_total

    if not validate_payment_info():
      return

    try:
      # First check inventory availability for all items before proceeding
      inventory_check_passed = True
      inventory_errors = []

      for item in cart_items:
        sci_id, qty, p_id, name, price, current_inventory = item

        # Check if product is still in stock with sufficient quantity
        if qty > current_inventory:
          inventory_check_passed = False
          if current_inventory > 0:
            inventory_errors.append(f"{name}: Only {current_inventory} available, you requested {qty}")
          else:
            inventory_errors.append(f"{name}: Out of stock")

      # If inventory check failed, show error and return
      if not inventory_check_passed:
        error_message = "Cannot place order due to inventory issues:\n" + "\n".join(inventory_errors)
        checkout_status.value = error_message
        return

      # Get next order ID
      c.execute("SELECT MAX(O_ID) FROM ORDERS")
      result = c.fetchone()
      new_order_id = 1 if result[0] is None else result[0] + 1

      # Create order in database
      order_date_query = "SELECT TO_CHAR(SYSDATE, 'DD-MON-YYYY') FROM DUAL"
      c.execute(order_date_query)
      order_date = c.fetchone()[0]

      # Format expiry date for database (assuming MM/YYYY input)
      expiry_parts = expiry_date_textbox.value.strip().split('/')
      expiry_date = f"01-{expiry_parts[0]}-{expiry_parts[1]}"  # 01-MM-YYYY

      # Set initial status
      initial_status = "Pending" if has_tradein_checkbox.value else "To be delivered"

      # Get remarks for trade-in
      trade_in_remarks = ""
      if has_tradein_checkbox.value:
        device_descriptions = []
        for device in tradein_devices:
          device_info = device['device_textbox'].value.strip()
          serial_info = device['serial_textbox'].value.strip()
          if device_info and serial_info:
            device_descriptions.append(f"{device_info} (S/N: {serial_info})")

        if device_descriptions:
          trade_in_remarks = f"Trade-in requested: {'; '.join(device_descriptions)}"
        else:
          trade_in_remarks = "Trade-in requested but details incomplete"
      else:
        trade_in_remarks = "NA"

      # Insert order record
      insert_order_query = """
      INSERT INTO ORDERS (O_ID, O_TOTAL_AMOUNT, O_DATE, CREDIT_CARD, CREDIT_DATE, CVC, O_STATUS, REMARKS, MEMBER_M_ID)
      VALUES (:o_id, :total, TO_DATE(:order_date, 'DD-MON-YYYY'), :cc, TO_DATE(:expiry, 'DD-MM-YYYY'), :cvc, :status, :remarks, :member_id)
      """

      order_values = {
        'o_id': new_order_id,
        'total': cart_total,
        'order_date': order_date,
        'cc': credit_card_textbox.value.strip().replace(' ', ''),
        'expiry': expiry_date,
        'cvc': cvc_textbox.value.strip(),
        'status': initial_status,
        'remarks': trade_in_remarks,
        'member_id': current_member['id']
      }

      c.execute(insert_order_query, order_values)

      # Create order lines for each item with optimistic locking
      for i, item in enumerate(cart_items):
        sci_id, qty, p_id, name, price, inventory = item

        # Get next order line ID
        c.execute("SELECT MAX(OL_ID) FROM ORDER_LINE")
        result = c.fetchone()
        new_ol_id = 1 if result[0] is None else result[0] + 1

        # Insert order line
        insert_ol_query = """
        INSERT INTO ORDER_LINE (OL_ID, OL_QTY, P_PRICE, PRODUCT_P_ID, ORDERS_O_ID)
        VALUES (:ol_id, :qty, :price, :product_id, :order_id)
        """

        ol_values = {
          'ol_id': new_ol_id + i,  # Increment for each item
          'qty': qty,
          'price': price,
          'product_id': p_id,
          'order_id': new_order_id
        }

        c.execute(insert_ol_query, ol_values)

        # Update product inventory with concurrency control
        # First check if inventory is still sufficient at time of update
        c.execute("""
          SELECT P_INVENTORY
          FROM PRODUCT
          WHERE P_ID = :p_id
        """, {'p_id': p_id})

        current_inventory = c.fetchone()[0]

        if current_inventory < qty:
          # Roll back transaction and report error
          c.execute("rollback")
          checkout_status.value = f"Error: {name} inventory changed during checkout. Only {current_inventory} available now."
          return

        # If inventory is still sufficient, update it
        c.execute("""
          UPDATE PRODUCT
          SET P_INVENTORY = P_INVENTORY - :qty
          WHERE P_ID = :p_id
        """, {'qty': qty, 'p_id': p_id})

        # Mark product as inactive if inventory reaches zero
        c.execute("""
          UPDATE PRODUCT
          SET P_STATUS = CASE
            WHEN P_INVENTORY <= 0 THEN 'Inactive'
            ELSE P_STATUS
          END
          WHERE P_ID = :p_id AND P_INVENTORY <= 0
        """, {'p_id': p_id})

      # If trade-in is requested, create trade-in device records
      if has_tradein_checkbox.value:
        for device in tradein_devices:
          device_desc = device['device_textbox'].value.strip()
          serial_num = device['serial_textbox'].value.strip()

          if device_desc and serial_num:
            # Get next trade-in ID
            c.execute("SELECT MAX(T_ID) FROM TRADE_IN_DEVICE")
            result = c.fetchone()
            new_trade_id = 1 if result[0] is None else result[0] + 1

            # Insert trade-in record (status pending until officer review)
            insert_trade_query = """
            INSERT INTO TRADE_IN_DEVICE (T_ID, SERIAL_NUMBER, CONDITION, TRADE_IN_PRICE, T_STATUS, ORDERS_O_ID, STAFF_S_ID)
            VALUES (:t_id, :serial, 'Pending Inspection', 0, 'Pending', :order_id, 1)
            """

            trade_values = {
              't_id': new_trade_id,
              'serial': serial_num,
              'order_id': new_order_id
            }

            c.execute(insert_trade_query, trade_values)

      # Delete items from shopping cart
      c.execute("""
        DELETE FROM SHOPPING_CART_ITEM
        WHERE MEMBER_M_ID = :member_id
      """, {'member_id': current_member['id']})

      # Commit all changes
      c.execute("commit")

      # Set success message for Message page
      message_title.value = "Order Placed Successfully!"
      message_label.value = f"Your order #{new_order_id} has been placed. You can check your order status anytime."

      # Update message context and button text
      message_context['return_to_member'] = True
      message_back_button.description = "Back to Member Menu"

      # Clear the cart items
      cart_items = []
      cart_total = 0

      # Show message page
      showPage("Message")

    except Exception as e:
      checkout_status.value = f"Error placing order: {str(e)}"
      try:
        c.execute("rollback")
      except:
        pass

  # Button handlers
  def on_place_order_btn_clicked(b):
    place_order()

  place_order_btn = widgets.Button(
    description="Place Order",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(place_order_btn, PRIMARY_COLOR)

  place_order_btn.on_click(on_place_order_btn_clicked)

  def on_back_to_cart_btn_clicked(b):
    showPage("Shopping Cart")

  back_to_cart_btn = widgets.Button(
    description="Back to Cart",
    layout=widgets.Layout(width='180px', height='35px')
  )
  style_button(back_to_cart_btn, SECONDARY_COLOR)

  back_to_cart_btn.on_click(on_back_to_cart_btn_clicked)

  # Layout the page with improved styling
  header_box = widgets.VBox([
    checkout_title,
    checkout_subtitle,
    widgets.HTML("<hr>")
  ])

  # Style form fields with consistent layout
  payment_form_style = widgets.Layout(
    display='flex',
    flex_flow='row',
    justify_content='space-between',
    width='100%',
    margin='5px 0'
  )

  payment_box = widgets.VBox([
    payment_section_label,
    widgets.HBox([credit_card_label, credit_card_textbox], layout=payment_form_style),
    widgets.HBox([expiry_date_label, expiry_date_textbox], layout=payment_form_style),
    widgets.HBox([cvc_label, cvc_textbox], layout=payment_form_style),
    SEPARATOR
  ])

  tradein_box = widgets.VBox([
    tradein_section_label,
    has_tradein_checkbox,
    tradein_devices_container,
    SEPARATOR
  ])

  # Status message with consistent styling
  status_box = widgets.HBox([checkout_status], layout=widgets.Layout(
    min_height='30px',
    padding='5px',
    margin='5px 0'
  ))

  # Buttons with consistent layout
  buttons_box = widgets.HBox([
    place_order_btn,
    back_to_cart_btn
  ], layout=widgets.Layout(
    justify_content='flex-start',
    margin='10px 0',
    spacing='20px'
  ))

  # Display all components with improved layout
  display(widgets.VBox([
    header_box,
    checkout_output,
    payment_box,
    tradein_box,
    status_box,
    buttons_box
  ], layout=widgets.Layout(
    padding='10px',
    width='100%'
  )))

  # Display order summary when checkout page is shown
  display_checkout_summary()

################ Checkout - End ######################



##########################################################
################ Order Status - Begin ######################
##########################################################

with tb_all.output_to('Order Status'):
    class OrderStatusSystem:
        def __init__(self):
            self.current_orders = []
            self.current_page = 0  # Track current page of orders
            self.current_member = None
            self.orders_per_page = 5  # Orders per page
            self.current_order_details = None  # Current order being viewed

            # Create UI widgets
            self.create_widgets()
            self.setup_handlers()
            self.clear_order_display()

        def create_widgets(self):
            """Initialize all UI widgets"""
            # Page title and subtitle
            self.OS_title = create_header("Browse Order History")
            self.OS_subtitle = create_subheader("View and manage your past orders")

            # Main page widgets
            self.OS_button1 = widgets.Button(
                description="Previous Page",
                disabled=True,
                layout=widgets.Layout(width='120px', height='30px'),
                style=widgets.ButtonStyle(button_color='#2196F3')  # Blue button
            )
            self.OS_button2 = widgets.Button(
                description="Next Page",
                disabled=True,
                layout=widgets.Layout(width='120px', height='30px'),
                style=widgets.ButtonStyle(button_color='#2196F3')  # Blue button
            )
            self.OS_button3 = widgets.Button(
                description="Back to Menu",
                layout=widgets.Layout(width='120px', height='30px'),
                style=widgets.ButtonStyle(button_color='#4CAF50')  # Green button
            )
            self.OS_spacer = widgets.HTML("<hr>")
            self.OS_page_info = widgets.Label("Page 0 of 0", style={'font_weight': 'bold'})
            self.OS_member_label = widgets.Label("Member: Not logged in",
                                              style={'font_weight': 'bold'})

            # Order containers (5 per page)
            self.order_containers = []
            for i in range(self.orders_per_page):
                order_box = widgets.VBox([
                    widgets.HBox([
                        widgets.Text(value='', description='Order ID:', disabled=True, layout=widgets.Layout(width='200px')),
                        widgets.Text(value='', description='Date:', disabled=True, layout=widgets.Layout(width='200px')),
                        widgets.Text(value='', description='Total:', disabled=True, layout=widgets.Layout(width='200px')),
                        widgets.Text(value='', description='Status:', disabled=True, layout=widgets.Layout(width='200px')),
                        widgets.Button(
                            description='View Details',
                            disabled=True,
                            layout=widgets.Layout(width='120px', height='30px'),
                            style=widgets.ButtonStyle(button_color='#4CAF50') # Green button
                        )
                    ])
                ])
                self.order_containers.append(order_box)

            # Main container
            self.main_container = widgets.VBox([
                self.OS_title,
                self.OS_subtitle,
                self.OS_spacer,
                self.OS_member_label,
                *self.order_containers,
                widgets.HBox([self.OS_button1, self.OS_button2, self.OS_page_info],
                           layout=widgets.Layout(justify_content='flex-start', padding='10px 0px')),
                widgets.HTML("<hr>"),
                self.OS_button3,
                widgets.HTML("<hr>")
            ])

        def setup_handlers(self):
            """Connect button click handlers"""
            self.OS_button1.on_click(self.on_previous_clicked)
            self.OS_button2.on_click(self.on_next_clicked)
            self.OS_button3.on_click(self.on_back_clicked)

            # Connect details button handlers
            for i, container in enumerate(self.order_containers):
                details_button = container.children[0].children[-1]
                details_button.on_click(self.create_details_handler(i))

        def create_details_handler(self, container_index):
            """Create handler for details button at given index"""
            def handler(b):
                order_idx = self.current_page * self.orders_per_page + container_index
                if order_idx < len(self.current_orders):
                    self.current_order_details = self.current_orders[order_idx]
                    self.show_order_details()
            return handler

        def show_order_details(self):
            """Display detailed view in the Order Details tab"""
            if not self.current_order_details:
                return

            # Clear and display styled order details
            with order_detail_output:
                order_detail_output.clear_output()

                # Create HTML content for styled display with only black text
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
                    <div style="background-color: #f5f5f5; padding: 10px; text-align: center;">
                        <h2 style="margin: 0;">ORDER DETAILS</h2>
                    </div>

                    <div style="margin: 20px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="font-weight: bold;">Order ID:</div>
                            <div>{self.current_order_details['O_ID']}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="font-weight: bold;">Date:</div>
                            <div>{self.format_date(self.current_order_details['O_DATE'])}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                            <div style="font-weight: bold;">Status:</div>
                            <div>{self.current_order_details['O_STATUS']}</div>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <div style="font-weight: bold;">Remarks:</div>
                            <div>{self.current_order_details['REMARKS'] or 'None'}</div>
                        </div>
                    </div>

                    <div style="margin: 20px 0;">
                        <h3 style="border-bottom: 1px solid #ddd; padding-bottom: 5px;">PRODUCTS</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background-color: #f5f5f5;">
                                    <th style="padding: 8px; text-align: left;">Product</th>
                                    <th style="padding: 8px; text-align: right;">Quantity</th>
                                    <th style="padding: 8px; text-align: right;">Unit Price</th>
                                    <th style="padding: 8px; text-align: right;">Subtotal</th>
                                </tr>
                            </thead>
                            <tbody>
                """

                # Add products to table
                if self.current_order_details.get('items'):
                    for item in self.current_order_details['items']:
                        try:
                            item_total = float(item['P_PRICE']) * int(item['OL_QTY'])
                            html_content += f"""
                                <tr style="border-bottom: 1px solid #eee;">
                                    <td style="padding: 8px;">{item['P_NAME']}</td>
                                    <td style="padding: 8px; text-align: right;">{item['OL_QTY']}</td>
                                    <td style="padding: 8px; text-align: right;">${float(item['P_PRICE']):.2f}</td>
                                    <td style="padding: 8px; text-align: right;">${item_total:.2f}</td>
                                </tr>
                            """
                        except Exception as e:
                            html_content += f"""
                                <tr>
                                    <td colspan="4" style="padding: 8px;">Error displaying product: {str(e)}</td>
                                </tr>
                            """

                    # Add products total
                    html_content += f"""
                                <tr style="font-weight: bold;">
                                    <td colspan="3" style="padding: 8px; text-align: right;">Total Price:</td>
                                    <td style="padding: 8px; text-align: right;">${float(self.current_order_details['O_TOTAL_AMOUNT']):.2f}</td>
                                </tr>
                            """
                else:
                    html_content += """
                                <tr>
                                    <td colspan="4" style="padding: 8px; text-align: center;">No products found in this order</td>
                                </tr>
                            """

                html_content += """
                            </tbody>
                        </table>
                    </div>
                """

                # Add trade-in section if applicable
                if self.current_order_details.get('items1'):
                    html_content += f"""
                    <div style="margin: 20px 0;">
                        <h3 style="border-bottom: 1px solid #ddd; padding-bottom: 5px;">TRADE-IN REQUESTS</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background-color: #f5f5f5;">
                                    <th style="padding: 8px; text-align: left;">Trade-in ID</th>
                                    <th style="padding: 8px; text-align: left;">Status</th>
                                    <th style="padding: 8px; text-align: right;">Discount</th>
                                </tr>
                            </thead>
                            <tbody>
                    """

                    tradein_discount = 0
                    for item in self.current_order_details['items1']:
                        try:
                            tradein_discount += float(item['TRADE_IN_PRICE'])
                            html_content += f"""
                                <tr style="border-bottom: 1px solid #eee;">
                                    <td style="padding: 8px;">{item['T_ID']}</td>
                                    <td style="padding: 8px;">{item['T_STATUS']}</td>
                                    <td style="padding: 8px; text-align: right;">${float(item['TRADE_IN_PRICE']):.2f}</td>
                                </tr>
                            """
                        except Exception as e:
                            html_content += f"""
                                <tr>
                                    <td colspan="3" style="padding: 8px;">Error displaying trade-in: {str(e)}</td>
                                </tr>
                            """

                    # Add trade-in totals
                    final_total = float(self.current_order_details['O_TOTAL_AMOUNT']) - tradein_discount
                    html_content += f"""
                            </tbody>
                        </table>
                        <div style="margin-top: 10px;">
                            <div style="display: flex; justify-content: space-between;">
                                <div style="font-weight: bold;">Trade-in Discount:</div>
                                <div>${tradein_discount:.2f}</div>
                            </div>
                            <div style="display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1em; margin-top: 5px;">
                                <div>Final Total After Discount:</div>
                                <div>${final_total:.2f}</div>
                            </div>
                        </div>
                    </div>
                    """

                html_content += "</div>"  # Close main container

                # Display the HTML content
                display(widgets.HTML(html_content))

            # Navigate to Order Details tab
            showPage("Order Details")

        def format_date(self, date_obj):
            """Format date object for display"""
            try:
                return date_obj.strftime('%d/%m/%Y')
            except (AttributeError, TypeError):
                return "N/A"

        def clear_order_display(self):
            """Clear all order information from display"""
            for container in self.order_containers:
                summary = container.children[0]
                for widget in summary.children[:-1]:  # Skip the details button
                    widget.value = ''
                summary.children[-1].disabled = True

            self.OS_button1.disabled = True
            self.OS_button2.disabled = True
            self.OS_page_info.value = "Page 0 of 0"
            # No need to update the spacer as it's now an HTML separator

        # Start with main view
        @property
        def current_view(self):
            return self.main_container

        def display_orders_page(self):
            """Display a page of orders (10 orders per page)"""
            if not self.current_orders:
                self.clear_order_display()
                self.OS_spacer.value = ""
                return

            total_pages = (len(self.current_orders) + self.orders_per_page - 1) // self.orders_per_page
            self.OS_page_info.value = f"Page {self.current_page + 1} of {total_pages}"

            start_idx = self.current_page * self.orders_per_page
            end_idx = min(start_idx + self.orders_per_page, len(self.current_orders))

            # Update navigation buttons
            self.OS_button1.disabled = (self.current_page == 0)
            self.OS_button2.disabled = (end_idx >= len(self.current_orders))

            # Display each order in its container
            for i in range(self.orders_per_page):
                order_idx = start_idx + i
                container = self.order_containers[i]
                summary = container.children[0]
                details_button = summary.children[-1]

                if order_idx < len(self.current_orders):
                    order = self.current_orders[order_idx]

                    # Update order summary
                    summary.children[0].value = str(order['O_ID'])
                    summary.children[1].value = self.format_date(order['O_DATE'])
                    summary.children[2].value = f"${order['O_TOTAL_AMOUNT']:.2f}"
                    summary.children[3].value = order['O_STATUS']

                    # Enable details button
                    details_button.disabled = False
                else:
                    # Clear this container if no order for this position
                    for widget in summary.children[:-1]:
                        widget.value = ''
                    details_button.disabled = True

        def fetch_orders(self, username):
            """Fetch all orders for the given username from database"""
            try:
                # Get member's orders
                c.execute("""
                    SELECT O_ID, O_DATE, O_TOTAL_AMOUNT, O_STATUS, REMARKS
                    FROM ORDERS
                    INNER JOIN MEMBER ON ORDERS.MEMBER_M_ID = MEMBER.M_ID
                    WHERE MEMBER.M_USERNAME = :username
                    ORDER BY O_DATE DESC, O_ID DESC
                """, {'username': username})

                orders = []
                for row in c.fetchall():
                    order = {
                        'O_ID': row[0],
                        'O_DATE': row[1],
                        'O_TOTAL_AMOUNT': row[2],
                        'O_STATUS': row[3],
                        'REMARKS': row[4],
                        'items': [],
                        'items1': []
                    }

                    # Get order items
                    c.execute("""
                        SELECT P.P_NAME, OL.OL_QTY, P.P_PRICE
                        FROM ORDER_LINE OL
                        JOIN PRODUCT P ON OL.PRODUCT_P_ID = P.P_ID
                        WHERE OL.ORDERS_O_ID = :order_id
                        ORDER BY OL.OL_ID
                    """, {'order_id': order['O_ID']})

                    for item_row in c.fetchall():
                        order['items'].append({
                            'P_NAME': item_row[0],
                            'OL_QTY': item_row[1],
                            'P_PRICE': item_row[2]
                        })

                    # Get trade-in devices
                    c.execute("""
                        SELECT T_ID, TRADE_IN_PRICE, T_STATUS
                        FROM TRADE_IN_DEVICE
                        WHERE ORDERS_O_ID = :order_id
                        ORDER BY T_ID
                    """, {'order_id': order['O_ID']})

                    for item_row in c.fetchall():
                        order['items1'].append({
                            'T_ID': item_row[0],
                            'TRADE_IN_PRICE': item_row[1],
                            'T_STATUS': item_row[2]
                        })

                    orders.append(order)

                return orders

            except Exception as e:
                print(f"Database error: {e}")
                return []

        def display_member_orders(self, member_info=None):
            """Display orders for the current member (can be called externally)"""
            if member_info:
                self.current_member = member_info
                self.OS_member_label.value = f"Member: {member_info.get('username', 'Unknown')}"
                self.OS_member_label.style = {'color': 'green', 'font_weight': 'bold'}

            if not self.current_member:
                self.OS_spacer.value = "No member information available"
                return

            self.current_orders = self.fetch_orders(self.current_member.get('username'))
            self.current_page = 0  # Reset to first page
            self.display_orders_page()

        def on_previous_clicked(self, b):
            """Handle Previous button click"""
            if self.current_page > 0:
                self.current_page -= 1
                self.display_orders_page()

        def on_next_clicked(self, b):
            """Handle Next button click"""
            max_page = (len(self.current_orders) + self.orders_per_page - 1) // self.orders_per_page - 1
            if self.current_page < max_page:
                self.current_page += 1
                self.display_orders_page()

        def on_back_clicked(self, b):
            """Handle Back button click"""
            showPage("Member")

    # Create and display the system
    order_system = OrderStatusSystem()

    # Make system available globally
    if 'order_system' not in globals():
        globals()['order_system'] = order_system

    display(order_system.main_container)

    # Auto-load orders if member info exists
    if 'current_member' in globals() and globals()['current_member']:
        order_system.display_member_orders(globals()['current_member'])

################ Order Status - End ######################


# Initialize by showing the Introduction tab (which now includes login)
showPage("Introduction")

##########################################################
################ Order Details - Begin ####################
##########################################################

with tb_all.output_to('Order Details'):
  # Order Details header with consistent styling but no colors
  order_detail_title = create_header("Order Details")
  order_detail_subtitle = create_subheader("View your order information below")

  # Create styled output area for order details
  order_detail_output = widgets.Output(layout={'border': '1px solid #e0e0e0', 'padding': '10px'})

  # Create back button without color styling
  order_detail_back_btn = widgets.Button(
      description="Back to Orders",
      layout=ACTION_BUTTON_LAYOUT
  )
  # Make Order Details button bold
  order_detail_back_btn.style = {'font_weight': 'bold'}

  # Status message area
  order_detail_status = create_styled_message("", "info")

  # Create layout with consistent spacing
  display(widgets.VBox([
      order_detail_title,
      order_detail_subtitle,
      SEPARATOR,
      order_detail_output,
      SECTION_SPACING,
      widgets.HBox([order_detail_back_btn]),
      order_detail_status,
      SEPARATOR
  ]))

  # Button handler
  def on_order_detail_back_btn_clicked(b):
    showPage("Order Status")
  order_detail_back_btn.on_click(on_order_detail_back_btn_clicked)

################ Order Details - End ######################

# Initialize by showing the Introduction tab (which now includes login)
showPage("Introduction")

c.close()
