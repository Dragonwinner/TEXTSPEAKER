"""
CSV processor for reading text entries and metadata for video generation.
"""
import csv
from pathlib import Path
from typing import List, Dict


def read_csv_texts(csv_path: str) -> List[Dict[str, str]]:
    """
    Read text entries from CSV file.
    
    Expected CSV format:
    - Column 1: 'text' - The text to be spoken by avatar
    - Column 2 (optional): 'filename' - Custom filename for output video (without extension)
    - Column 3 (optional): 'avatar' - Path to specific avatar image (if different from default)
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        List of dictionaries containing text and metadata for each entry
        
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV format is invalid
    """
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    entries = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Check if 'text' column exists
        if 'text' not in reader.fieldnames:
            raise ValueError("CSV must have a 'text' column")
        
        for idx, row in enumerate(reader, start=1):
            text = row.get('text', '').strip()
            
            if not text:
                print(f"Warning: Skipping empty text at row {idx}")
                continue
            
            entry = {
                'text': text,
                'filename': row.get('filename', '').strip() or f"video_{idx}",
                'avatar': row.get('avatar', '').strip() or None,
                'row_number': idx
            }
            
            entries.append(entry)
    
    return entries


def validate_csv_format(csv_path: str) -> bool:
    """
    Validate that CSV file has the correct format.
    
    Args:
        csv_path: Path to the CSV file
        
    Returns:
        True if format is valid, False otherwise
    """
    try:
        csv_file = Path(csv_path)
        if not csv_file.exists():
            print(f"Error: CSV file not found: {csv_path}")
            return False
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if not reader.fieldnames:
                print("Error: CSV file is empty")
                return False
            
            if 'text' not in reader.fieldnames:
                print("Error: CSV must have a 'text' column")
                return False
            
            # Read at least one row to validate
            try:
                row = next(reader)
                if not row.get('text', '').strip():
                    print("Warning: First row has empty text")
            except StopIteration:
                print("Warning: CSV has no data rows")
        
        return True
        
    except Exception as e:
        print(f"Error validating CSV: {e}")
        return False
