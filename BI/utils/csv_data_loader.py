import csv
import logging
from datetime import datetime
from typing import Generator, Dict, Any
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
                    try:
                        row["amount"] = float(row["amount"])
                        row["timestamp"] = datetime.fromisoformat(row["timestamp"])
                        row["is_fraud"] = str(row["is_fraud"]).strip().lower() in ("true", "1")
                        yield row
                    except (ValueError, KeyError) as e:
                        logger.warning("Error de formato en la fila %d: %s", row_number, e)
        except FileNotFoundError as e:
            logger.error("No se encontró el archivo en la ruta: %s", self._file_path)
            raise