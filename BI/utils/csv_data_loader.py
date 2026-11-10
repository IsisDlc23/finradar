import csv
import logging
from datetime import datetime
from typing import Generator, Dict, Any
feature/Correccion-de-transacciones
from pathlib import Path

logger = logging.getLogger(__name__)

class CsvDataLoader:
    def __init__(self, file_path=None) -> None:
        if file_path is None:
            # Apunta automáticamente a BI/data/transactions.csv sin importar la carpeta actual
            self._file_path = Path(__file__).parent.parent / "data" / "transactions.csv"
        else:
            self._file_path = Path(file_path)

    def read(self) -> Generator[Dict[str, Any], None, None]:
        """Lee el archivo CSV fila por fila utilizando un generador."""
        try:
            with open(self._file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row_number, row in enumerate(reader, start=2):
=======

from domain.exceptions import DataLoaderError

logger = logging.getLogger(__name__)


class CsvDataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Generator[Dict[str, Any], None, None]:
        try:
 