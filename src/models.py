from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, field_validator
# Request and Response validation using Pydantic models.


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


class ExpenseCreate(BaseModel):
    """The fields a client supplies when creating an expense."""

    title: str
    amount: float = Field(gt=0)
    category: Category
    date: date

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, title: str) -> str:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValueError("title must not be blank")
        return cleaned_title
