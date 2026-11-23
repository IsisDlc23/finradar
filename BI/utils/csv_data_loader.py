import csv
import logging
from datetime import datetime
from typing import Generator, Dict, Any
from pathlib import Path
from domain.exceptions import DataLoaderError

logger = logging.getLogger(__name__)

class CsvDataLoader:
    def __init__(self, file_path=None) -> None:
        # Apunta automáticamente a BI/data/transactions.csv sin importar la carpeta actual
        if file_path is None:
            self.file_path = Path(__file__).parent.parent / "data" / "transactions.csv"
        else:
            self.file_path = Path(file_path)

    def read(self) -> Generator[Dict[str, Any], None, None]:
        """Lee el archivo CSV fila por fila utilizando un generador."""
        try:

            with open(self.file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row_number, row in enumerate(reader, start=2):
                    yield row
        except Exception as e:
            logger.error(f"Error al leer el archivo CSV en {self.file_path}: {e}")
            
            
            