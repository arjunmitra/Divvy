from typing import List, Dict
from datetime import datetime
from Member import Member
class Order:
    def __init__(self, transactionDate : datetime, location : str, subtotals : Dict[str, float], totalWithTax: float):
        # String name of purchase location
        self._location : str = location
        # Date object of when transaction occurred
        self._date : datetime = transactionDate
        # Float total value of order with tax
        self._total: float = totalWithTax
        # List of Member objects
        self._members : List[Member] = self.splitTotal(subtotals)

    def setLocation(self, location : str):
        self._location = location

    # Returns name of location/restaurant
    def getLocation(self) -> str:
        return self._location

    def setMembers(self, members : List[Member]):
        self._members = members

    # Returns list of participants' costs as Member objects
    def getMembers(self) -> List[Member]:
        return self._members

    def setDate(self, transaction_date : datetime):
        self._date = transaction_date

    # Returns date of transaction
    def getDate(self) -> datetime:
        return self._date

    # Returns total price of order with tax
    def getTotal(self) -> float:
        return self._total

    def splitTotal(self, subtotals : Dict[str, float]) -> List[Member]:
        totalNoTax : float = sum([subtotals[memberName] for memberName in subtotals])
        members : List[Member] = list()
        for memberName in subtotals:
            memberSubtotal = subtotals[memberName]/totalNoTax * self._total
            members.append(Member(memberName, memberSubtotal))
        return members

    def __str__(self) ->  str:
        message = "Transaction Date: " +  str(self._date)
        message += "\nLocation/Restaurant: " + self._location
        message += "\nTotal: $" + str(round(self.getTotal(), 2)) + '\n'
        for member in self._members:
            message += "\n" + str(member)
        return message