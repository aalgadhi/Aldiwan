import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx2pdf import convert
from os import system
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # Import PhotoImage to use an image as the icon

harakat = [character for character in "ًٌٍَُِّْ"] # All of the harakat

def baitPrinter(alsader, alajs):
    # Define the total width for each half of the verse
    shater_length = 40 # Half of a line length

    alsaderLength = 0
    for character in alsader:
        if character not in harakat:
            alsaderLength += 1

    alajsLength = 0
    for character in alajs:
        if character not in harakat:
            alajsLength += 1
    
    # alsaderMargins = int((shater_length - alsaderLength)/2) * '*'
    # alajsMargins = int((shater_length - alajsLength)/2) * '*'
    # bait = f"{alsaderMargins + alsader + alsaderMargins}     {alajsMargins + alajs + alajsMargins}"
    bait = f"{alsader}{10*' '}{alajs}"
    return bait


def generate_qasida_pdf():
    # Get the URL from the entry field
    url = url_entry.get()
    
    # Check if URL is empty
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return

    # Send a GET request to fetch the HTML content of the page
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Create a new Document
        doc = Document()
        
        # Qasida information
        qasida_info = soup.find("h2").get_text().split("»")
        matlaa_alqasida = qasida_info[-1].strip()  # First line of the poetry
        alshaer = qasida_info[-2].strip()  # The poet
        matlaa_alqasida_splitted = "_".join(map(str, matlaa_alqasida.split()))
        alshaer_splitted = "_".join(map(str, alshaer.split()))
        # Add poet name as heading
        doc.add_heading(alshaer + "\n", level=0).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

        # Locate the div with id "poem_content" and find all h3 tags within it
        poem_content = soup.find("div", id="poem_content")
        if poem_content:
            h3_tags = poem_content.find_all("h3")

            # Loop through h3 tags in pairs to form verses
            for i in range(int(len(h3_tags) / 2)):
                alsader = h3_tags[2 * i].get_text().strip()  # First half of the line
                alajs = h3_tags[2 * i + 1].get_text().strip()  # Second half of the line
                paragraph = doc.add_paragraph(
                    baitPrinter(alsader, alajs)
                )
                paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Center the paragraph
                paragraph.style.font.size = Pt(16)  # Set font size if needed
            
            # Generate file names
            system(f"mkdir qasidas")
            file_name = f"{matlaa_alqasida_splitted}_{alshaer_splitted}"
            docx_filename = f"qasidas/{file_name}.docx"
            pdf_filename = f"qasidas/{file_name}.pdf"

            # Save the document as a .docx file
            doc.save(docx_filename)

            # Convert the .docx file to a PDF
            convert(docx_filename, pdf_filename)

            # Open the PDF file
            system(f"start {pdf_filename}")
            messagebox.showinfo("Success", f"'{pdf_filename}' حفظت القصيد بالملف: ")
        else:
            messagebox.showerror("Content Error", "القصيدة يجب أن تكون من موقع الديوان")
    else:
        messagebox.showerror("Request Error", f"Failed to retrieve the page. Status code: {response.status_code}")

# Create the GUI window
root = tk.Tk()
root.title("Qasida PDF Generator")

# Set the window icon to "logo.ico" for both title bar and taskbar
root.iconbitmap("logo.ico")

# URL input label and entry field
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=0, padx=10, pady=10)

tk.Label(root, text=":الصق الرابط من موقع الديوان").grid(row=0, column=1, padx=10, pady=10)

# Generate PDF button
generate_button = tk.Button(root, text="ابدأ", command=generate_qasida_pdf)
generate_button.grid(row=1, column=0, columnspan=2, pady=10)

# Run the GUI
root.mainloop()