from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_transactions():
    # Add Transaction 1: DANNON +300 points
    response = client.post("/add", json={
        "payer": "DANNON",
        "points": 300,
        "timestamp": "2022-10-31T10:00:00Z"
    })
    assert response.status_code == 200

    # Add Transaction 2: UNILEVER +200 points
    response = client.post("/add", json={
        "payer": "UNILEVER",
        "points": 200,
        "timestamp": "2022-10-31T11:00:00Z"
    })
    assert response.status_code == 200

    # Add Transaction 3: DANNON -200 points
    response = client.post("/add", json={
        "payer": "DANNON",
        "points": -200,
        "timestamp": "2022-10-31T15:00:00Z"
    })
    assert response.status_code == 200

    # Add Transaction 4: MILLER COORS +10000 points
    response = client.post("/add", json={
        "payer": "MILLER COORS",
        "points": 10000,
        "timestamp": "2022-11-01T14:00:00Z"
    })
    assert response.status_code == 200

    # Add Transaction 5: DANNON +1000 points
    response = client.post("/add", json={
        "payer": "DANNON",
        "points": 1000,
        "timestamp": "2022-11-02T14:00:00Z"
    })
    assert response.status_code == 200

    # Spend Points: 5000 points
    response = client.post("/spend", json={"points": 5000})
    assert response.status_code == 200
    assert response.json() == [
        { "payer": "DANNON", "points": -100 },
        { "payer": "UNILEVER", "points": -200 },
        { "payer": "MILLER COORS", "points": -4700 }
    ]

    # Check Final Balances
    response = client.get("/balance")
    assert response.status_code == 200
    assert response.json() == {
        "DANNON": 1000,
        "UNILEVER": 0,
        "MILLER COORS": 5300
    }

    print("All tests passed successfully.")

if __name__ == "__main__":
    test_transactions()
