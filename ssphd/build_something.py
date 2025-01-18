import os
import subprocess
from pathlib import Path

def process(input_file: str) -> None:
    """
    Process the input markdown file and generate outputs.
    
    Args:
        input_file: Path to the markdown file to process
    """
    input_path = Path(input_file)
    base_name = input_path.stem
    
    formats = ["html"]  # Add more formats as they become supported
    
    for fmt in formats:
        output_dir = f"{base_name}-{fmt}"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = Path(output_dir) / f"{base_name}.{fmt}"
        _run_pandoc(input_path, output_file, fmt)

def _run_pandoc(input_file: Path, output_file: Path, format: str) -> None:
    """Run pandoc with appropriate filters and options."""
    cmd = [
        "pandoc",
        str(input_file),
        "-o", str(output_file),
        "--filter=pandoc-sidenote",
        "--filter=pandoc-crossref"
    ]
    subprocess.run(cmd, check=True)
