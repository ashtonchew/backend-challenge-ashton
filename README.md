# backend-challenge-ashton

This README provides instructions on how to set up, run, and test the API project.

## How to Run the Code

### 1. Install Dependencies

- Ensure you have Python 3.7 or higher installed.
- Install FastAPI and Uvicorn using pip:

```
pip install fastapi uvicorn
```

### 2. Run the Application

- Use Uvicorn to run the app on port 8000:

```
uvicorn main:app --reload --port 8000
```

### 3. Test the API

- You can use tools like **curl** or **Postman** to interact with the API.
- Alternatively, navigate to `http://localhost:8000/docs` to access the automatic Swagger UI and test the endpoints interactively.

## Running Test Cases

To run the test cases, use the following command:

```
python test_api.py
```

This will execute all the test cases defined in the `test_api.py` file.

## License

n/a
