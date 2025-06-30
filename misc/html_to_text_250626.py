import argparse #handles command-line input
from bs4 import BeautifulSoup #HTML parser
import os #basic os tools 

def extract_table_text(soup):
    rows = [] #collects each row of table as line of text

    for tr in soup.find_all('tr'): #loop through all tr elements (table elements)
        cells = tr.find_all(['td', 'th'])
        cell_values = [cell.get_text(strip=True) for cell in cells] #extract text from each cell and strip whitespace
        row_text = '\t'.join(cell_values)

        if row_text:
            rows.append(row_text)

    return '\n'.join(rows)


def convert_html_to_text(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file: #opens .html file for reading
        html_content = file.read()

    soup = BeautifulSoup(html_content,'html.parser') 
    raw_text = extract_table_text(soup)

    lines = [line.strip() for line in raw_text.splitlines()] #breaks the full text into lines and strips extra spaces at beginning or end of each line
    cleaned_text = '\n'.join([line for line in lines if line]) #puts claned lines together and skips empty lines

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as out_file: #saves the file to .txt
        out_file.write(cleaned_text)

    print(f"saved cleaned text to {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert HTML to clean text.') #handles and creates arguments when running the script
    parser.add_argument('--input', required=True) #to type in the input HTML file
    parser.add_argument('--output', required=True) #to type path output .txt is saved to
    args = parser.parse_args() #grabs the values typed above

    if not os.path.isfile(args.input):
        print(f"input file not found: {args.input}")
    else:
        convert_html_to_text(args.input, args.output)
    


