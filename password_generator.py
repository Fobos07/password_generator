"""
This script is a PyQt5-based password generator and manager application.

It allows users to generate strong passwords, save them with custom names,
copy passwords to the clipboard, and delete saved passwords.

It also displays a list of saved passwords for quick access.

Requirements:
- PyQt6 for GUI
- pyperclip for clipboard operations
"""

from random import choice
import json

from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QMessageBox, QInputDialog

import pyperclip

# Load the UI design from 'main.ui' file
Form, Window = uic.loadUiType('src/windows/main.ui')

app = QApplication([])  # Create an instance of QApplication
window = Window()  # Create an instance of the main window
form = Form()  # Create an instance of the UI form generated from the UI file
form.setupUi(window)  # Configure the UI form on the main window


def change_slider(value):
    """
    Update the displayed password length when the slider value changes.

    Args:
        value (int): The new slider value representing password length.
    """
    form.pswd_length.setHtml(
        f'''<div style="text-align: center;vertical-align: middle;">
         <font size="50">{value}</font>
         </div>'''
    )


def generate_password():
    """
    Generate a password based on user-selected options and display it.
    """
    password = ''
    symbols = 'abcdefghijklmnopqrstuvwxyz'
    if form.checkBox.isChecked():
        symbols += '0123456789'
    if form.checkBox_2.isChecked():
        symbols += '!@#$*-_'
    if form.checkBox_3.isChecked():
        symbols += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for _ in range(int(form.pswd_length.toPlainText())):
        password += choice(symbols)
    form.final_password.setHtml(
        f'''<div style="text-align: center; vertical-align: middle;">
        <font size="5">{password}</font>
        </div>'''
    )


def show_popup():
    """
    Show a dialog to save the generated password with a custom name.
    """
    text, ok_btn = QInputDialog.getText(
        None,
        "Save Password",
        "Enter a name for the password:"
    )
    if ok_btn:
        msg = QMessageBox()
        msg.setWindowTitle("Save Password")
        msg.setText(f"Password saved as: {text}")
        msg.setIcon(QMessageBox.Information)
        msg.setStandardButtons(QMessageBox.Ok)
        with open('src/data/pswds.json', 'r', encoding='utf-8') as pwd_file:
            current_pswrds: dict = json.load(pwd_file)
        current_pswrds.update({text: form.final_password.toPlainText()})
        with open('src/data/pswds.json', 'w', encoding='utf-8') as pwd_file:
            pwd_file.write(json.dumps(current_pswrds))
        generate_current_pswrds()
        msg.exec_()


def crnt_pswrd():
    """
    Display the selected saved password in the UI.
    """
    with open('src/data/pswds.json', 'r', encoding='utf-8') as pwd_file:
        pswrd = json.load(pwd_file).get(form.current_psrds.currentText())
    form.saved_password.setText(pswrd)


def copy_pswrd():
    """
    Copy the displayed saved password to the clipboard and show a confirmation message.
    """
    pyperclip.copy(form.saved_password.toPlainText())
    msg = QMessageBox()
    msg.setText("Password copied to clipboard!")
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.exec_()


def delete_pswrd():
    """
    Delete the selected saved password and update the displayed list of saved passwords.
    """
    with open('src/data/pswds.json', 'r', encoding='utf-8') as pwd_file:
        curent_pswrds: dict = json.load(pwd_file)
    curent_pswrds.pop(form.current_psrds.currentText())
    with open('src/data/pswds.json', 'w', encoding='utf-8') as pwd_file:
        pwd_file.write(json.dumps(curent_pswrds))
    generate_current_pswrds()
    form.current_psrds.setCurrentIndex(0)


def generate_current_pswrds():
    """
    Load and display the list of saved passwords in the UI.
    """
    with open('src/data/pswds.json', 'r', encoding='utf-8') as pwd_file:
        current_pswrds: dict = json.load(pwd_file)
    form.current_psrds.clear()
    form.current_psrds.addItem('')
    for i in current_pswrds.keys():
        form.current_psrds.addItem(i)


# Connect UI elements to functions
form.horizontalSlider.valueChanged.connect(change_slider)
form.generate_pswd.clicked.connect(generate_password)
form.save_pswd_btn.clicked.connect(show_popup)
generate_current_pswrds()
form.current_psrds.currentIndexChanged.connect(crnt_pswrd)
form.copy_pswrd.clicked.connect(copy_pswrd)
form.delate_pswrd.clicked.connect(delete_pswrd)

window.setWindowIcon(QIcon('src/data/key.ico'))
window.show()  # Display the main window
app.exec()
