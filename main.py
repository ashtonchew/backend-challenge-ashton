from fastapi import FastAPI, HTTPException
from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from collections import defaultdict

app = FastAPI()


class Transaction(BaseModel):
    payer: str
    points: int
    timestamp: datetime

class SpendRequest(BaseModel):
    points: int

class SpendResponse(BaseModel):
    payer: str
    points: int


transactions = []  
balances = defaultdict(int)  

@app.post("/add", status_code=200)
def add_points(transaction: Transaction):
    balances[transaction.payer] += transaction.points

    # Postprocess negative transactions to ensure all positive points are recorded first,
    # simplifying the deduction logic and maintaining transaction order for FIFO spending
    if transaction.points < 0:
        points_to_deduct = -transaction.points
        remaining_deduct = points_to_deduct

        if balances[transaction.payer] < 0:
            balances[transaction.payer] -= transaction.points
            raise HTTPException(status_code=400, detail=f"Not enough points for payer {transaction.payer}.")

        for t in transactions:
            if t["payer"] == transaction.payer and t["points"] > 0:
                available_points = t["points"]
                deduction = min(available_points, remaining_deduct)
                t["points"] -= deduction
                remaining_deduct -= deduction
                if remaining_deduct == 0:
                    break
    else:
        transactions.append({
            "payer": transaction.payer,
            "points": transaction.points,
            "timestamp": transaction.timestamp
        })

    return

@app.post("/spend", response_model=List[SpendResponse], status_code=200)
def spend_points(request: SpendRequest):
    total_points = sum(balances.values())
    if total_points < request.points:
        raise HTTPException(status_code=400, detail="Not enough points to spend.")
    
    # FIFO for spend is a predictable approach to point deduction (i.e. aligns with user expectations)
    sorted_transactions = sorted(transactions, key=lambda x: x['timestamp'])
    points_to_spend = request.points
    spent_points = defaultdict(int)

    for t in sorted_transactions:
        if points_to_spend == 0:
            break
        if t['points'] <= 0:
            continue

        available_points = t['points']
        deduction = min(available_points, points_to_spend)
        t['points'] -= deduction
        balances[t['payer']] -= deduction
        spent_points[t['payer']] -= deduction
        points_to_spend -= deduction

    return [{"payer": payer, "points": points} for payer, points in spent_points.items()]

@app.get("/balance", status_code=200)
def get_balance():
    return balances
