from datetime import date
from enum import Enum

from pydantic import BaseModel


class Category(str, Enum):
    """Categories accepted by the expense tracker."""

    FOOD = "food"
    TRANSPORT = "transport"
    BILLS = "bills"
    SHOPPING = "shopping"
    OTHER = "other"


class Expense(BaseModel):
    """An expense returned by the API."""

    id: int
    title: str
    amount: float
    category: Category
    date: date
