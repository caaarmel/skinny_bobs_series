"""
This script processes HTML files containing tournament data, extracts relevant information from tables (including optional headings and data rows), and converts them into tab-delimited text files. Processed HTML files are then archived. The script expects HTML files in the '../import' directory, outputs cleaned text files to '../import/raw', and moves processed HTML files to '../import/archive'.

    - Scans import/raw/ for any .html files.
    - Parses each .html file using BeautifulSoup.
    - Extracts the <h3> title (optional), header row (once), and all valid player rows (rows with 11 cells).
    - Writes the cleaned .txt version to import/cleaned/ using the same filename as the original HTML.
    - Moves the original .html file to import/archived/.   

"""

from bs4 import BeautifulSoup #HTML parser
import os #basic os tools 
import shutil #file operations
from config import RAW_HTML_DIR, RAW_TXT_DIR, ARCHIVE_DIR  #import paths from config

# Define base directories
INPUT_DIR = RAW_HTML_DIR #input directory for HTML files
OUTPUT_DIR = RAW_TXT_DIR #output directory for cleaned text files

# Ensure output and archive directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True) #creates output directory if it doesn't exist
os.makedirs(ARCHIVE_DIR, exist_ok=True) #creates archive directory if it doesn't exist

def is_data_row(row_data):
    return len(row_data) == 11 #checks if the row has exactly 11 columns, which is the expected format for data rows

def convert_html_to_txt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file: #opens the input HTML file for reading
        soup = BeautifulSoup(file, 'html.parser') #parses the HTML content using BeautifulSoup  

    body = soup.find("body")
    if not body:
        print(f"No body found in {input_path}. Skipping file.")
        return False
    
    lines = []

    #optional heading
    h3 = body.find('h3') #finds the first h3 element in the body
    if h3:
        lines.append(h3.get_text(strip=True)) #extracts text from h3 and strips whitespace
    
    header_written = False #flag to track if the header has been written

    for table in body.find_all("table"): #finds all table elements in the body
        for tr in table.find_all("tr"): #loops through each row in the table
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])] #extracts text from each cell in the row and strips whitespace
            
            if not header_written and cells and cells[0].strip().upper() == "TOURNEY": #checks if the first cell is "TOURNEY" to identify the header row
                lines.append('\t'.join(cells)) #joins the cell values with tabs and adds to lines list
                header_written = True #sets the flag to True after writing the header
            elif is_data_row(cells) and header_written and cells and cells[0].strip().upper() != "TOURNEY": #checks if the row has the correct number of columns
                lines.append('\t'.join(cells)) #joins the cell values with tabs and adds to lines list
            

    if not lines: #if no lines were collected, return False
        print(f"No valid data found in {input_path}. Skipping file.")
        return False
    
    with open(output_path, 'w', encoding='utf-8') as out_file: #opens the output file for writing
        out_file.write('\n'.join(lines)) #writes the collected lines to the output file

    return True #indicates successful conversion

def main():
    html_files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(".html")] #lists all HTML files in the input directory

    if not html_files: #checks if there are no HTML files
        print("No HTML files found in the input directory: {}".format(INPUT_DIR))
        return
    
    for filename in html_files: #iterates through each HTML file
        input_path = os.path.join(INPUT_DIR, filename) #constructs the full path for the input file
        base_name = os.path.splitext(filename)[0] #gets the base name of the file without extension
        output_path = os.path.join(OUTPUT_DIR, f"{base_name}.txt") #constructs the full path for the output file
        archive_path = os.path.join(ARCHIVE_DIR, filename) #constructs the full path for the archive file

        print(f"Processing {filename}...") #prints the name of the file being processed
        success = convert_html_to_txt(input_path, output_path) #calls the conversion function

        if success:
            shutil.move(input_path, archive_path) #moves the processed file to the archive directory
            print(f"Converted {filename} to {output_path} and archived the original file.")
        else:
            print(f"Failed to convert {filename}. Skipping archiving.")

if __name__ == '__main__':
    main() #calls the main function to start the script