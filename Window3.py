import sys
import csv
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt

class Window3(QWidget):
    def __init__(self, tiempos_secuencial, tiempos_paralelo):
        super().__init__()
        self.tiempos_secuencial = tiempos_secuencial
        self.tiempos_paralelo = tiempos_paralelo
        
        self.setWindowTitle('Window 3')
        self.resize(1000, 700)

        # Layout configuration
        layout = QVBoxLayout()

        # Download Button 
        self.downloadButton = QPushButton('Download as CSV')
        self.downloadButton.setFixedSize(200, 50)
        self.downloadButton.clicked.connect(self.downloadButtonClick)
        
        # Plot widget with PyQtGraph
        self.plotWidget = pg.PlotWidget()
        layout.addWidget(self.plotWidget)

        self.plotData()  # Plot initial data

        # Add widgets to layout
        layout.addWidget(self.downloadButton)
        self.setLayout(layout)

        print('secuential')
        print(self.tiempos_secuencial)
        print('parallell')
        print(self.tiempos_paralelo)

    def plotData(self):
        # Clear previous plots
        self.plotWidget.clear()

        # Plot data using PyQtGraph
        self.plotWidget.plot(self.tiempos_secuencial, pen='b', name='Secuential')
        self.plotWidget.plot(self.tiempos_paralelo, pen='r', name='Parallel')

        # Set labels and title
        self.plotWidget.setLabel('left', 'Time (ms)')
        self.plotWidget.setLabel('bottom', 'Iteration')
        self.plotWidget.setTitle('Execution Time Comparison')

    def downloadButtonClick(self):
        # Implement CSV download logic as before
        filename = 'execution_times.csv'
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Secuential', 'Parallel'])
                for seq, par in zip(self.tiempos_secuencial, self.tiempos_paralelo):
                    writer.writerow([seq, par])
            print(f"CSV file '{filename}' written successfully.")

        except IOError as e:
            print(f"Error writing CSV file: {e}")

