from pdftocsv import pdftocsv
from train import train
from aibot import bot

# Converting PDFs
print("Convertendo PDFs to CSVs")
pdftocsv('csv-files')

# Training ChatBot
print("Training")
train()

# Executing Bot
print("Executing")
bot()