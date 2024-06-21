import sys
import csv
from PyQt6.QtWidgets import QWidget, QVBoxLayout,QLineEdit, QHBoxLayout, QGridLayout, QPushButton, QLabel, QTextEdit, QFileDialog
from PyQt6.QtCore import Qt
import pandas as pd
import concurrent.futures
import time
from Window3 import Window3

class Window2(QWidget):
    def __init__(self, df, lista):
        super().__init__()
        self.df = df 
        self.lista = lista
        self.sorted_list = []
        self.tiempos = []
        self.tiempos_secuencial = []
        self.tiempos_paralelo = []
        self.tiempos_quick_secuencial = []
        self.tiempos_quick_paralelo = []

        self.setWindowTitle('Window 2')
        self.resize(1000, 700)

        # Layout config
        layout = QVBoxLayout()
        # Sublayout config
        sublayout = QHBoxLayout()

        # Layout Widgets
            ## Title
        self.title = QLabel('SORTING OPTIONS')
        self.title.setStyleSheet('font-size: 28px; font-weight: bold;')

            ## Preview Dialog
        self.previewDialog = QTextEdit()
        self.previewDialog.setReadOnly(True)
            ## Log
        self.log = QLabel(" Execution Time")
        self.log.setStyleSheet('font-size: 24px; font-weight: normal;')
            ## Download Button 
        self.downloadButton= QPushButton('Download as csv')
        self.downloadButton.setFixedSize(200,50)
        self.downloadButton.clicked.connect(self.downloadButtonClick)
        # Add widgets to layout
        layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addLayout(sublayout)
        layout.addWidget(self.previewDialog)
        layout.addWidget(self.log)
        layout.addWidget(self.downloadButton)

        # Sublayout widgets 
            ## Merge Secuential Button 
        self.mergeSecuentialButton= QPushButton('MergeSort Secuential')
        self.mergeSecuentialButton.setFixedSize(200,50)
        self.mergeSecuentialButton.clicked.connect(self.mergeSecuentialButtonClick)
        
            ## Merge Parallell Button
        self.mergeParallellButton = QPushButton('MergeSort Parallell')
        self.mergeParallellButton.setFixedSize(200,50)
        self.mergeParallellButton.clicked.connect(self.mergeParallellButtonClick)

            ## Merge Secuential Button 
        self.quickSecuentialButton= QPushButton('QuickSort Secuential')
        self.quickSecuentialButton.setFixedSize(200,50)
        self.quickSecuentialButton.clicked.connect(self.quickSecuentialButtonClick)
            ## Quick Parallell Button
        self.quickParallellButton = QPushButton('QuickSort Parallell')
        self.quickParallellButton.setFixedSize(200,50)
        self.quickParallellButton.clicked.connect(self.quickParallellButtonClick)

        ## Compare Button 
        self.compareButton= QPushButton('Compare')
        self.compareButton.setFixedSize(200,50)
        self.compareButton.clicked.connect(self.compareButtonClick)
        
        
        # Add sublayout widgets
        sublayout.addWidget(self.mergeSecuentialButton)
        sublayout.addWidget(self.mergeParallellButton)
        sublayout.addWidget(self.quickSecuentialButton)
        sublayout.addWidget(self.quickParallellButton)
        sublayout.addWidget(self.compareButton)

        # Set general Layout
        self.setLayout(layout)
    
    # When Merge Secuential Button Click 
    def mergeSecuentialButtonClick(self):

        self.sorted_list = self.apply_merge_sort_secuential(self.tiempos)
        self.display_sorted_data(self.sorted_list)      
    
    # Merge Sort to df 
    def apply_merge_sort_secuential(self,times):
        print(self.lista)
        start_time = time.time()
        sorted_list = self.merge_sort(self.lista)
        end_time = time.time()  # Toma el tiempo de finalización
        execution_time = (end_time - start_time)*1000
        times.append(execution_time)     

        print(sorted_list)
        return sorted_list
    
    # Display Sorted Data
    def display_sorted_data(self, sorted_values):
        sorted_text = ', '.join(map(str, sorted_values))
        self.previewDialog.setPlainText(sorted_text)
        self.log.setText(f'Execution Time: {self.tiempos[0]:.6f} ms')
        self.tiempos.clear()

    # Merge Sort
    def merge_sort(self,arr):
        def convertir_a_entero(elemento):
            try:
                return int(elemento)
            except ValueError:
                return float('inf')  # Si no se puede convertir, devuelve infinito

        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]     # Sublista izquierda
            R = arr[mid:]     # Sublista derecha

            self.merge_sort(L)     # Ordena la sublista izquierda
            self.merge_sort(R)     # Ordena la sublista derecha

            # Fusiona las sublistas ordenadas
            i = j = k = 0
            while i < len(L) and j < len(R):
                if convertir_a_entero(L[i]) <= convertir_a_entero(R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            # Agrega cualquier elemento restante de L (si los hay)
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            # Agrega cualquier elemento restante de R (si los hay)
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
        
        return arr


### MERGE PARALLELL
# When Merge Parallell Button Click 
    def mergeParallellButtonClick(self):

        self.sorted_list = self.apply_merge_sort_parallell(self.tiempos)
        self.display_sorted_data_parallell(self.sorted_list)      
    
    # Apply Merge Sort to list 
    def apply_merge_sort_parallell(self,times):
        print(self.lista)
        start_time = time.time()
        sorted_list = self.merge_sort_parallell(self.lista)
        end_time = time.time()  # Toma el tiempo de finalización
        execution_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        times.append(execution_time)

        print(sorted_list)

        return sorted_list
    
    # Merge Sort Parallell

    def merge_sort_parallell(self, arr):
        
        def convertir_a_entero(elemento):
            try:
                return int(elemento)
            except ValueError:
                return float('inf')  # Si no se puede convertir, devuelve infinito

        if len(arr) > 1:
            mid = len(arr) // 2
            L = arr[:mid]     # Sublista izquierda
            R = arr[mid:]     # Sublista derecha

            # Ordenar las sublistas en paralelo
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futureL = executor.submit(self.merge_sort, L)
                futureR = executor.submit(self.merge_sort, R)
                L = futureL.result()
                R = futureR.result()

            # Fusiona las sublistas ordenadas
            i = j = k = 0
            while i < len(L) and j < len(R):
                if convertir_a_entero(L[i]) <= convertir_a_entero(R[j]):
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            # Agrega cualquier elemento restante de L (si los hay)
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            # Agrega cualquier elemento restante de R (si los hay)
            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1

        return arr
    
    def display_sorted_data_parallell(self, sorted_values):
        sorted_text = ', '.join(map(str, sorted_values))
        self.previewDialog.setPlainText(sorted_text)
        self.log.setText(f'Execution Time: {self.tiempos[0]:.6f} ms')
        self.tiempos.clear()

# When quick Secuential Button Click 
    def quickSecuentialButtonClick(self):

        self.sorted_list = self.apply_quick_sort_secuential(self.tiempos)
        self.display_quick_sorted_data(self.sorted_list)      
    
    # quick Sort to list
    def apply_quick_sort_secuential(self,times):
        print(self.lista)
        start_time = time.time()
        sorted_list = self.quick_sort(self.lista)
        end_time = time.time()  # Toma el tiempo de finalización
        execution_time = (end_time - start_time)*1000
        times.append(execution_time)     

        print(sorted_list)
        return sorted_list
    
    # Display Sorted Data
    def display_quick_sorted_data(self, sorted_values):
        sorted_text = ', '.join(map(str, sorted_values))
        self.previewDialog.setPlainText(sorted_text)
        self.log.setText(f'Execution Time: {self.tiempos[0]:.6f} ms')
        self.tiempos.clear()

    # quick Sort
    def quick_sort(self, arr):
        def convertir_a_entero(elemento):
            try:
                return int(elemento)
            except ValueError:
                return float('inf')  # Si no se puede convertir, devuelve infinito

        def partition(low, high):
            pivot = arr[high]  # Elegimos el último elemento como pivote
            pivot_value = convertir_a_entero(pivot)
            i = low - 1
    
            for j in range(low, high):
                if convertir_a_entero(arr[j]) <= pivot_value:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
    
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quick_sort_iterative(arr):
            # Crear una pila para almacenar los límites del arreglo
            stack = []
            stack.append(0)  # Índice bajo
            stack.append(len(arr) - 1)  # Índice alto
    
            # Iterar mientras la pila no esté vacía
            while stack:
                high = stack.pop()
                low = stack.pop()
    
                # Obtener el índice del pivote
                pi = partition(low, high)
    
                # Si hay elementos a la izquierda del pivote, agregarlos a la pila
                if pi - 1 > low:
                    stack.append(low)
                    stack.append(pi - 1)
    
                # Si hay elementos a la derecha del pivote, agregarlos a la pila
                if pi + 1 < high:
                    stack.append(pi + 1)
                    stack.append(high)
    
        quick_sort_iterative(arr)
        return arr



# When Quick Parallell Button Click 
    def quickParallellButtonClick(self):

        self.sorted_list = self.apply_quick_sort_parallell(self.tiempos)
        self.display_quick_sorted_data_parallell(self.sorted_list)      
    
    # Apply Merge Sort to list 
    def apply_quick_sort_parallell(self,times):
        print(self.lista)
        start_time = time.time()
        sorted_list = self.quick_sort_parallell(self.lista)
        end_time = time.time()  # Toma el tiempo de finalización
        execution_time = (end_time - start_time) * 1000  # Convertir a milisegundos
        times.append(execution_time)

        print(sorted_list)

        return sorted_list
    

    # quick sort parallell
    def quick_sort_parallell(self, arr):
        def convertir_a_entero(elemento):
            try:
                return int(elemento)
            except ValueError:
                return float('inf')  # Si no se puede convertir, devuelve infinito

        def partition(arr, low, high):
            pivot = arr[high]  # Elegimos el último elemento como pivote
            pivot_value = convertir_a_entero(pivot)
            i = low - 1

            for j in range(low, high):
                if convertir_a_entero(arr[j]) <= pivot_value:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]

            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            return i + 1

        def quick_sort_recursive(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)
                quick_sort_recursive(arr, low, pi - 1)
                quick_sort_recursive(arr, pi + 1, high)

        def parallel_sort(arr, low, high):
            if low < high:
                pi = partition(arr, low, high)

                # Ejecutar las sublistas en paralelo
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future1 = executor.submit(parallel_sort, arr, low, pi - 1)
                    future2 = executor.submit(parallel_sort, arr, pi + 1, high)

                    # Esperar a que ambas tareas terminen
                    concurrent.futures.wait([future1, future2])

        parallel_sort(arr, 0, len(arr) - 1)
        return arr
    
    def display_quick_sorted_data_parallell(self, sorted_values):
        sorted_text = ', '.join(map(str, sorted_values))
        self.previewDialog.setPlainText(sorted_text)
        self.log.setText(f'Execution Time: {self.tiempos[0]:.6f} ms')
        self.tiempos.clear()

    def showWindow3(self):
        self.window3 = Window3(self.tiempos_secuencial, self.tiempos_paralelo, self.tiempos_quick_secuencial, self.tiempos_quick_paralelo)
        self.window3.show()

    # When compare button click 
    def compareButtonClick(self):
        for i in range(30):
            sortedList = self.apply_merge_sort_secuential(self.tiempos_secuencial)
            sortedList2 = self.apply_merge_sort_parallell(self.tiempos_paralelo)
            sortedList3 = self.apply_quick_sort_secuential(self.tiempos_quick_secuencial)
            sortedList4 = self.apply_quick_sort_parallell(self.tiempos_quick_paralelo)
        self.showWindow3()
    
    # When download button click 
    def downloadButtonClick(self):
        if not self.sorted_list:
            print("Empty list, cannot generate a csv, sort first.")
            return

        # Nombre del archivo CSV de salida
        filename = 'sorted_data.csv'
        stringList = [str(num) for num in self.sorted_list]
        # Escribir los datos en el archivo CSV
        try:
            with open(filename, mode='w', newline='') as file:
                writer = csv.writer(file, delimiter=' ')
                writer.writerows(stringList)
            print(f"Archivo CSV '{filename}' escrito correctamente.")

        except IOError as e:
            print(f"Error al escribir el archivo CSV: {e}")

    
    