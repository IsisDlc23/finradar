import logging
from typing import Dict, List
from pymongo.errors import PyMongoError
 
from domain.exceptions import RepositoryError
from domain.transaction import Transaction
 
logger = logging.getLogger(__name__)
 
 
class MongoTransactionRepository:
 
    def __init__(self, database) -> None:
        self._collection = database["transactions"]
 
    def find_by_filter(self, filters: dict, limit: int = 1_000) -> List[Transaction]:
        try:
            cursor = self._collection.find(filters, {"_id": 0}).limit(limit)
            return [Transaction.from_document(doc) for doc in cursor]
        except PyMongoError as error:
            logger.exception("Error en find_by_filter: %s", filters)
            raise RepositoryError("Error al consultar transacciones") from error
 
    def count(self, filters: dict = None) -> int:
        try:
            return self._collection.count_documents(filters or {})
        except PyMongoError as error:
            logger.exception("Error en count")
            raise RepositoryError("Error al contar transacciones") from error
 
    def total_amount_by_category(self) -> Dict[str, float]:
        pipeline = [
            {"$group": {"_id": "$merchant_category", "total": {"$sum": "$amount"}}},
            {"$sort": {"total": -1}},
        ]
        try:
            return {
                doc["_id"]: round(doc["total"], 2)
                for doc in self._collection.aggregate(pipeline)
            }
        except PyMongoError as error:
            logger.exception("Error en total_amount_by_category")
            raise RepositoryError("Error al agrupar por categoria") from error