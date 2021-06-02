from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from graphviz import Digraph
import welcomescreen


class Morsiphier(QDialog):
    def __init__(self,widget):
        super(Morsiphier, self).__init__()
        loadUi('gui/morsiphier.ui', self)
        self.widget=widget
        self.widget.setFixedWidth(1110)
        self.back_button.clicked.connect(self.back_to_menu)
        self.back_button.setIcon(QtGui.QIcon('icons/back.png'))
        self.back_button.setIconSize(QtCore.QSize(30, 30))
        self.encrypt_btn.clicked.connect(self.encrypt)
        self.decrypt_btn.clicked.connect(self.decrypt)
        self.clear_all_encrypt.clicked.connect(self.clear_encrypt)
        self.clear_all_decrypt.clicked.connect(self.clear_decrypt)

        self.MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                    'C': '-.-.', 'D': '-..', 'E': '.',
                    'F': '..-.', 'G': '--.', 'H': '....',
                    'I': '..', 'J': '.---', 'K': '-.-',
                    'L': '.-..', 'M': '--', 'N': '-.',
                    'O': '---', 'P': '.--.', 'Q': '--.-',
                    'R': '.-.', 'S': '...', 'T': '-',
                    'U': '..-', 'V': '...-', 'W': '.--',
                    'X': '-..-', 'Y': '-.--', 'Z': '--..',
                    '1': '.----', '2': '..---', '3': '...--',
                    '4': '....-', '5': '.....', '6': '-....',
                    '7': '--...', '8': '---..', '9': '----.',
                    '0': '-----', ', ': '--..--', '.': '.-.-.-',
                    '?': '..--..', '/': '-..-.', '-': '-....-',
                    '(': '-.--.', ')': '-.--.-'}

    def clear_encrypt(self):
        self.encrypt_data.clear()

    def clear_decrypt(self):
        self.decrypt_data.clear()

    def decrypt(self):
        text_to_decrypt = self.decrypt_data.toPlainText()
        decrypted_text = ''
        encrypted_word = ''
        if text_to_decrypt != '':
            text_to_decrypt+=' '
            for symbol in text_to_decrypt:
                if symbol != ' ':
                    i = 0
                    encrypted_word += symbol
                    
                else:
                    i += 1

                    if i == 2:
                        decrypted_text += ' '
                    else:
                        decrypted_text += list(self.MORSE_CODE_DICT.keys())[list(self.MORSE_CODE_DICT.values()).index(encrypted_word)]
                        encrypted_word = ''
        else:
            welcomescreen.execute_message_box("Enter input data","Input Data Warning")
            return
        
        self.encrypt_data.setText(decrypted_text)

    def encrypt(self):
        text_to_encrypt=self.encrypt_data.toPlainText()
        encrypted_text=''
        if text_to_encrypt.isupper():
            if text_to_encrypt!='':
                for letter in text_to_encrypt:
                    if letter!=' ':
                        if letter in self.MORSE_CODE_DICT.keys():
                            encrypted_text+=self.MORSE_CODE_DICT[letter]+' '
                        else:
                            welcomescreen.execute_message_box('Cannot encrypt the letter -> '+letter,"Input Data Warning")
                            return
                    else:
                        encrypted_text+=' '
            else:
                welcomescreen.execute_message_box("Enter input data","Input Data Warning")
                return
        else:
            welcomescreen.execute_message_box("Use only CAPITAL letters","Input Data Warning")
            return

        self.decrypt_data.setText(encrypted_text)
        
    def back_to_menu(self):
        welcome=welcomescreen.WelcomeScreen(self.widget)
        self.widget.addWidget(welcome)
        self.widget.setFixedWidth(1000)     
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)    
          