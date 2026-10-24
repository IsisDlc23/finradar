import csv
from datetime import datetime
from typing import Generator, Dict, Any
 
 
class CsvDataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path
 
    def read(self) -> Generator[Dict[str, Any], None, None]:
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row["amount"] = float(row["amount"])
                row["timestamp"] = datetime.fromisoformat(row["timestamp"])
                row["is_fraud"] = str(row["is_fraud"]).strip().lower() in ("true", "1")
                yield row