
import pyautogui
import time

pyautogui.PAUSE = 1
link = "https://www.duolingo.com/learn"

# abrir o navegador (chrome)
pyautogui.press("win")
pyautogui.write("Microsoft Edge")
pyautogui.press("enter")

# entrar no link 
pyautogui.write(link)
pyautogui.press("enter")
time.sleep(3)      

pyautogui.click(x=50, y=281) # Logo pra treinar escuta 

pyautogui.click(x=314, y=338) # Começar tarefa
time.sleep(3)   

# Tarefa 1
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 2
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 3
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 4
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 5
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 6
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 7
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 8
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 9
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 10
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

# Tarefa 11
pyautogui.click(x=126, y=966) # Pular
pyautogui.click(x=829, y=974) # Verificar

pyautogui.click(x=814, y=951) # Continuar
time.sleep(2)  
pyautogui.click(x=47, y=120) # Continuar
time.sleep(2)  
pyautogui.click(x=828, y=945) # Continuar
pyautogui.click(x=831, y=958) # Continuar
time.sleep(3)   

#Encerramos
import tkinter as tk
from tkinter import messagebox

# Cria a janela oculta
root = tk.Tk()
root.withdraw()  # esconde a janela principal

# Mostra a mensagem
messagebox.showinfo("Aviso", "Ofensiva Mantida!!\nEncerrando Programa!!")


