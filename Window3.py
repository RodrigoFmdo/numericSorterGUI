import sys
import csv
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt6.QtCore import Qt

class Window3(QWidget):
    def __init__(self, tiempos_secuencial, tiempos_paralelo, tqs,tqp):
        super().__init__()
        self.tiempos_secuencial = tiempos_secuencial
        self.tiempos_paralelo = tiempos_paralelo
        self.tqs = tqs
        self.tqp = tqp
        
        self.setWindowTitle('Window 3')
        self.resize(1000, 700)

        # Layout configuration
        layout = QVBoxLayout()

        # Download Button 
        self.downloadButton = QPushButton('Download timetable as CSV')
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
        print('quick sec')
        print(self.tqs)
        print("quick parallell")
        print(self.tqp)

    def plotData(self):
        # Clear previous plots
        self.plotWidget.clear()
        if hasattr(self, 'legend'):
            self.legend.scene().removeItem(self.legend)
        legend = self.plotWidget.addLegend()

        # Plot data using PyQtGraph
        l1 =self.plotWidget.plot(self.tiempos_secuencial, pen='b', name='Merge Secuential')
        l2 = self.plotWidget.plot(self.tiempos_paralelo, pen='r', name='Merge Parallel')
        l3 = self.plotWidget.plot(self.tqs, pen='g', name='Quick Secuential')
        l4 = self.plotWidget.plot(self.tqp, pen='y', name='Quick Parallel')

        legend.addItem(l1, 'Merge Sequential')
        legend.addItem(l2, 'Merge Parallel')
        legend.addItem(l3, 'Quick Sequential')
        legend.addItem(l4, 'Quick Parallel')

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
                writer.writerow(['Merge Secuential', 'Merge Parallel', 'Quick Secuential','Quick Parallell'] )
                for merseq, merpar, quickseq, quickpar in zip(self.tiempos_secuencial, self.tiempos_paralelo,self.tqs,self.tqp):
                    writer.writerow([merseq, merpar, quickseq, quickpar])
            print(f"CSV file '{filename}' written successfully.")

        except IOError as e:
            print(f"Error writing CSV file: {e}")

