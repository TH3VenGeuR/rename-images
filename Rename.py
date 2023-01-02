#!/usr/bin/python3

# Rename Images with Date Photo Taken

# Purpose: Renames image files in a folder based on date photo taken from EXIF metadata

# Author: Matthew Renze

# Usage: python.exe Rename.py input-folder
#   - input-folder = (optional) the directory containing the image files to be renamed

# Examples: python.exe Rename.py C:\Photos
#           python.exe Rename.py

# Behavior:
#  - Given a photo named "Photo Apr 01, 5 54 17 PM.jpg"  
#  - with EXIF date taken of "4/1/2018 5:54:17 PM"  
#  - when you run this script on its parent folder
#  - then it will be renamed "20180401-175417.jpg"

# Notes:
#   - For safety, please make a backup before running this script
#   - Currently only designed to work with .jpg, .jpeg, and .png files
#   - EXIF metadata must exist or an error will occur
#   - If you omit the input folder, then the current working directory will be used instead.

# Import libraries
import os
import sys
from pathlib import Path
from PIL import Image

import PySimpleGUI as sg

# Set dict for month in different language
month_languages = {
  "fr": {
    "1": "janvier",
    "2": "février",
    "3": "mars",
    "4": "avril",
    "5": "mai",
    "6": "juin",
    "7": "juillet",
    "8": "aout",
    "9": "septembre",
    "10": "octobre",
    "11": "novembre",
    "12": "décembre"
  },
  "en": {
    "1": "january",
    "2": "february",
    "3": "march",
    "4": "april",
    "5": "may",
    "6": "june",
    "7": "july",
    "8": "august",
    "9": "september",
    "10": "october",
    "11": "november",
    "12": "december"
  },
  "de": {
    "1": "januar",
    "2": "februar",
    "3": "märz",
    "4": "april",
    "5": "mai",
    "6": "juni",
    "7": "juli",
    "8": "august",
    "9": "september",
    "10": "oktober",
    "11": "november",
    "12": "dezember"
  },
  "it": {
    "1": "gennaio",
    "2": "febbraio",
    "3": "marzo",
    "4": "aprile",
    "5": "maggio",
    "6": "giugno",
    "7": "luglio",
    "8": "agosto",
    "9": "settembre",
    "10": "ottobre",
    "11": "novembre",
    "12": "dicembre"
  },
  "es": {
    "1": "enero",
    "2": "febrero",
    "3": "marzo",
    "4": "april",
    "5": "mayo",
    "6": "junio",
    "7": "julio",
    "8": "agosto",
    "9": "septiembre",
    "10": "octubre",
    "11": "noviembre",
    "12": "diciembre"
  }
}

layout = [
    [sg.Text("Select a folder:")],
    [sg.Input(), sg.FolderBrowse()],
    [sg.Text("Select a language:")],
    [sg.Radio("French", "LANGUAGE", key="fr", default=True)],
    [sg.Radio("English", "LANGUAGE", key="en")],
    [sg.Radio("German", "LANGUAGE", key="de")],
    [sg.Radio("Italian", "LANGUAGE", key="it")],
    [sg.Radio("Spanish", "LANGUAGE", key="es")],
    [sg.Text("Select a format:")],
    [sg.Radio("YYYYMMDD-HHmmss", "FORMAT", key="yyyymmdd")],
    [sg.Radio("31décembre01", "FORMAT", key="daymonthinc", default=True)],
    [sg.Button("Execute"), sg.Button("Cancel")]
]

# create the window and show it
window = sg.Window("Folder Picker", layout)
while True:
    # read the events in the window
    event, values = window.read()
    print(values)
    if event == "Execute":
        # do something with the selected folder, language and format
        folder_path = values[0]
        if values["en"]==True:
            language = "en"
        elif values["es"]==True:
            language = "es"
        elif values["it"]==True:
            language = "it"
        elif values["fr"]==True:
            language = "fr"
        elif values["de"]==True:
            language = "de"

        if values["yyyymmdd"]==True:
          date_format = "yyyymmdd"
        elif values["daymonthinc"]==True:
          date_format = "daymonthinc"

        # Set list of valid file extensions
        valid_extensions = [".jpg", ".jpeg", ".png"]

        #if len(sys.argv) < 1:
        #    folder_path = input_file_path = sys.argv[1]
        #else:
        #    folder_path = os.getcwd()
        
        # Get all files from folder
        file_names = os.listdir(folder_path)
        
        mydict = {}
        for file_name in file_names:
            # Create the old file path
            old_file_path = os.path.join(folder_path, file_name)
            # Open the image
            image = Image.open(old_file_path)
            # Get the date taken from EXIF metadata
            date_taken = image._getexif()[36867]
            mydict[file_name] = date_taken
            
        date_day = ""
        for key in sorted(mydict):
            old_date_day = date_day
            print(old_date_day)
            #print(key)
            # Get the file extension
            file_ext = os.path.splitext(key)[1]
        
            # If the file does not have a valid file extension
            # then skip it
            if (file_ext not in valid_extensions):
                continue
        
            # Create the old file path
            old_file_path = os.path.join(folder_path, key)
        
            # Open the image
            image = Image.open(old_file_path)
        
            # Get the date taken from EXIF metadata
            date_taken = image._getexif()[36867]
        
            # Close the image
            image.close()
            
            if date_format == "daymonthinc":
              date_day = date_taken.replace(" ",":").split(":")[2]
              date_month = date_taken.replace(" ",":").split(":")[1]
              month_in_letter =  month_languages.get(language, {}).get(date_month)
        
              # Reformat the date taken to "YYYYMMDD-HHmmss"
              #date_time = date_taken \
              #    .replace(":", "")      \
              #    .replace(" ", "-")
              date_time = date_day + month_in_letter
        
              if not old_date_day:
                  inc = 1 
              elif old_date_day != date_day:
                  inc = 1
              # Combine the new file name and file extension
              if os.path.exists(date_time + str(inc) + file_ext) == False:
                new_file_name = date_time + str(inc) + file_ext
                inc += 1
              else: 
                inc += 1
                new_file_name = date_time + str(inc) + file_ext
        
              # Create the new folder path
              new_file_path = os.path.join(folder_path, new_file_name)
            elif date_format== "yyyymmdd":

                date_time = date_taken \
                    .replace(":", "")      \
                    .replace(" ", "-")
            
                # Combine the new file name and file extension
                new_file_name = date_time + file_ext
            
                # Create the new folder path
                new_file_path = os.path.join(folder_path, new_file_name)
            # Rename the file
            os.rename(old_file_path, new_file_path)
            window.close()
    elif event == "Cancel" or event == sg.WIN_CLOSED:
        break

# close the window
window.close()

