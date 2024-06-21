import sys
import csv
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QLineEdit, QHBoxLayout, QGridLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PyQt6.QtCore import Qt
import pandas as pd
from Window2 import Window2

class Window1(QWidget):

    def __init__(self):
        super().__init__()
        self.df = None
        self.lista = []
        # Window config
        self.setWindowTitle('Window 1')
        self.resize(1000, 700)
        
        # Layout config
        layout = QVBoxLayout()

        # Sublayout config
        sublayout = QGridLayout()
        # sublayout.setContentsMargins(10,10,10,50)

        # Subsublayout config
        subsublayout = QHBoxLayout()
        sublayout2 = QHBoxLayout()
        
        # Layout Widgets
            ## Title
        self.title = QLabel('PARALLELL SORTING IMPLEMENTATIONS')
        self.title.setStyleSheet('font-size: 28px; font-weight: bold;')
        
            ## Log
        self.log = QLabel("!! Load your numeric database, Only csv/xlsx supported")
        self.log.setStyleSheet('font-size: 24px; font-weight: normal;')
        
        # Add widgets to layout
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)

        layout.addLayout(sublayout)
        layout.addLayout(sublayout2)
        layout.addWidget(self.log)

        # Sublayout widgets
            ## Preview Dialog
        self.previewDialog = QTextEdit()
        self.previewDialog.setReadOnly(True)

        # Add widgets to sublayout
        sublayout.addLayout(subsublayout,0,0)
        sublayout.addWidget(self.previewDialog,2,0)

        # Sublayout2 widgets 
            ## Validate Button 
        self.validateFileButton= QPushButton('validate Numeric File')
        self.validateFileButton.setFixedSize(200,50)
        self.validateFileButton.clicked.connect(self.onValidateFileButtonClick)
             ## Sort Button 
        self.sortFileButton= QPushButton('sort File')
        self.sortFileButton.setFixedSize(200,50)
        self.sortFileButton.clicked.connect(self.onSortFileButtonClick)

        ## Add sublayout2 widgets
        sublayout2.addWidget(self.validateFileButton)
        sublayout2.addWidget(self.sortFileButton)
        
        # Subsublayout widgets
            ## Path Line
        self.pathFile = QLineEdit() 

            ## Load File Button 
        self.loadFileButton= QPushButton('Browse file')
        self.loadFileButton.setFixedSize(200,50)
        self.loadFileButton.clicked.connect(self.onLoadFileButtonClick)

        ## Add subsublayout widgets
        subsublayout.addWidget(self.pathFile)
        subsublayout.addWidget(self.loadFileButton)

        # Set layout
        self.setLayout(layout)
    

    # When Load File Button Click
    def onLoadFileButtonClick(self):
        path = self.pathFile.text()
        if path:
            try:
                if path.endswith('.csv'):
                    self.df = pd.read_csv(path)

                    with open(path, newline='') as csvfile:
                     # Crear un lector CSV
                         lector = csv.reader(csvfile)
                         for fila in lector:
                             self.lista.append(fila[0])

                elif path.endswith('.xlsx'):
                    self.df = pd.read_excel(path)
                else:
                    raise ValueError("Selected file is not an XLSX or a CSV.")
                
                preview_text = self.df.head(100).to_string(index=False)
                self.previewDialog.setPlainText(preview_text)
                self.log.setText("File Loaded Succesfully. Please press Validate, or Sort button.")
            
            except Exception as e:
                self.log.setText(f"Error while opening file: {str(e)}")
                print(f"Error: {e}")
        else:
            self.log.setText("Please set a Path .")

    ## Validate Numeric df
    def validate_all_numeric(self):
        for position in self.df.columns:
            if not pd.to_numeric(self.df[position], errors='coerce').notnull().all():
                return False, position
        return True, None
    
    # When Validate File Button Click
    def onValidateFileButtonClick(self):
        if self.df is not None:
            valid, position = self.validate_all_numeric()
            if not valid:
                self.log.setText(f"Validation Error: Position '{position}' contains non-numeric data.")
                return 
            self.log.setText("File Validated Successfully. Please press Sort button.")
        else:
            self.log.setText("Please load a file first.")

    # When Sort File Button Click
    def onSortFileButtonClick(self):
        if self.df is not None:
            self.window2 = Window2(self.df, self.lista)
            self.window2.show()
        else:
            self.log.setText("Please load a file first.")
