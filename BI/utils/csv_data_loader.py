import csv
import logging
from datetime import datetime
from typing import Generator, Dict, Any

from domain.exceptions import DataLoaderError

logger = logging.getLogger(__name__)


class CsvDataLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> Generator[Dict[str, Any], None, None]:
        try:
            with open(self.file_path, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        row["amount"] = float(row["amount"])
                        row["timestamp"] = datetime.fromisoformat(row["timestamp"])
                        row["is_fraud"] = str(row["is_fraud"]).strip().lower() in ("true", "1")
                        yield row
                    except (ValueError, KeyError) as e:
                        logger.exception("Error al parsear fila en CSV: %s", row)
                        raise DataLoaderError("Formato de fila inválido en el archivo CSV") from e
        except FileNotFoundError as e:
            logger.exception("Archivo no encontrado: %s", self.file_path)
            raise DataLoaderError(f"No se encontró el archivo: {self.file_path}") from e
        except DataLoaderError:
            raise
        except Exception as e:
            logger.exception("Error inesperado leyendo el archivo CSV: %s", self.file_path)
            raise DataLoaderError("Fallo inesperado al leer el dataset") from e