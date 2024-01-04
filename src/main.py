from fastapi import FastAPI, HTTPException
import fitz  # Ensure PyMuPDF is installed for fitz
import json
import logging
import csv
import os
from generative_ai import process_text_with_ai  # Ensure this is defined or correctly imported
from redaction import redaction  # Ensure this is defined or correctly imported

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

def write_pii_to_csv(ai_output_list, csv_file_path):
    try:
        if not isinstance(ai_output_list, list):
            ai_output_list = [ai_output_list]

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Type", "Value", "Context"])  # CSV Header

            for ai_output in ai_output_list:
                try:
                    data = ai_output if isinstance(ai_output, dict) else json.loads(ai_output.strip()) if ai_output else {}
                    for pii_item in data.get('pii', []):
                        # Check 'value' is not empty and not NoneType, and 'is_value_pii' is true
                        if isinstance(pii_item, dict) and pii_item.get('value') and pii_item.get('is_value_pii', False):
                            row = [pii_item.get('type', ''), pii_item.get('value', ''), pii_item.get('context', '')]
                            logger.info(f"Preparing to write to CSV, row: {row}")
                            writer.writerow(row)
                except json.JSONDecodeError as e:
                    logger.error(f"Error decoding JSON for item: {ai_output}. Error: {e}")
    except Exception as e:
        logger.error(f"Error writing to CSV: {e}")
        raise e

def extract_data_to_mask(ai_output):
    try:
        if not ai_output:  # Return empty list if ai_output is None or empty
            return []

        data = ai_output if isinstance(ai_output, dict) else json.loads(ai_output.strip()) if ai_output else {}
        return [item.get('value') for item in data.get('pii', []) if item.get('value') is not None]
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        return []
    except (TypeError, KeyError) as e:
        logger.error(f"Error processing: {e}")
        return []

@app.post("/process-pdf")
async def process_pdf(input_pdf_path: str):
    try:
        doc = fitz.open(input_pdf_path)
        if not doc:
            raise HTTPException(status_code=400, detail="Document cannot be opened or is empty.")

        # Dynamically define the output CSV and pdf paths by appending -PREVIEW before the file extension and changing it to .csv
        base_name, _ = os.path.splitext(input_pdf_path)
        preview_report_path = f"{base_name}-PREVIEW.csv"
        output_pdf_path = f"{base_name}-PREVIEW.pdf"

        all_ai_outputs = []

        for page_num, page in enumerate(doc):
            text_to_analyse = page.get_text()
            ai_output = process_text_with_ai(text_to_analyse, ai_api="local")
            logger.info(f"AI Output for page {page_num}: {ai_output}")

            if ai_output:  # Ensure ai_output is not None
                all_ai_outputs.append(ai_output)

        # Remove duplicates and ensure meaningful data in all_ai_outputs
        unique_outputs = {json.dumps(ai, sort_keys=True) for ai in all_ai_outputs if ai}  # Remove None before converting to json
        cleaned_outputs = [json.loads(uo) for uo in unique_outputs]
        cleaned_outputs = [co for co in cleaned_outputs if any(co.get('pii', []))]

        if cleaned_outputs:
            logger.info(f"Preparing to write to CSV, data: {cleaned_outputs}")
            write_pii_to_csv(cleaned_outputs, preview_report_path)

        # Read back values from CSV for masking
        all_values_to_mask = []
        with open(preview_report_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                all_values_to_mask.append(row["Value"])  # Assumes column name in CSV is 'Value'
        # Garantir que todos os valores são strings
        all_values_to_mask = [str(value) for value in all_values_to_mask]
        
        redaction(input_pdf_path, output_pdf_path, all_values_to_mask)
        
        return {"message": "PDF processed successfully", "output_csv": preview_report_path, "output_pdf": output_pdf_path}

    except fitz.fitz.FileOpenError as e:  # Corrected exception handling
        logger.error(f"Failed to open document: {e}")
        raise HTTPException(status_code=400, detail="Failed to open document")
    except Exception as e:
        logger.error(f"Error during processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))
