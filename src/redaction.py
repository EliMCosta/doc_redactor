import fitz

def redaction(original_pdf_path, output_pdf_path, all_values_to_mask):
    # opening the pdf
    doc = fitz.open(original_pdf_path)

    # iterating through pages
    for page in doc:
        for data in all_values_to_mask:
            areas = page.search_for(data)
            
            # drawing outline over sensitive datas
            [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]
            
        # applying the redaction
        page.apply_redactions()
        
    # saving it to a new pdf
    doc.save(output_pdf_path)
    print("Successfully redacted")
