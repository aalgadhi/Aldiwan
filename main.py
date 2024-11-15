import requests
from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx2pdf import convert
from os import system

# Replace "your_url_here" with the actual URL you want to scrape
url = "https://www.aldiwan.net/poem4432.html#"

# Send a GET request to fetch the HTML content of the page
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Create a new Document
    doc = Document()
    doc.add_heading("Extracted H3 Tags", level=1).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
    
    # Find all h3 tags and add each to the document, center-aligned
    h3_tags = soup.find_all("h3")
    for h3 in h3_tags:
        paragraph = doc.add_paragraph(h3.get_text())
        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER  # Center the paragraph
        paragraph.style.font.size = Pt(12)  # Set font size if needed
    
    qasida_info = soup.find("h2").get_text().split("»")
    matlaa_alqasida = qasida_info[-1].strip()  # First line of the poetry
    alshaer = qasida_info[-2].strip()  # The poet
    matlaa_alqasida_splitted = "_".join(map(str, matlaa_alqasida.split()))

    file_name = f"{matlaa_alqasida_splitted}_{alshaer}"

    # Save the document as a .docx file
    docx_filename = f"{file_name}.docx"
    doc.save(docx_filename)

    # Convert the .docx file to a PDF
    pdf_filename = f"{file_name}.pdf"
    convert(docx_filename, pdf_filename)
    
    system(f"start {pdf_filename}")
    print(f"The qasida has been saved to '{pdf_filename}' as a PDF")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
