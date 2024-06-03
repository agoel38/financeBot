try:
    from pdfminer.high_level import extract_text_to_fp
    print("pdfminer.six is installed correctly.")
except ImportError as e:
    print(f"Error: {e}")
