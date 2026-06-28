# .env variables

1. DB_URL="postgresql+asyncpg://postgres:password@localhost:5432/M2A1"
2. environment="dev"
3. Title="M2A1"

# .env.test variables

1. DB_URL="postgresql+asyncpg://postgres:password@localhost:5432/M2A1_test"
2. environment="test"

# Instructions to execute Question 1.

Run this command at the root of the folder

uv run uvicorn main.src:app --reload

1. Access your desired web-browser and put in this url 
"http://localhost:8000/docs" you will get fastApi client 


# Instructions to execute Question 2.

Run this command at the root of the folder

1. uv run pytest tests/test_main.py -v


# Instructions to execute Question 3.

Run this command at the root of the folder

make sure k6 is already installed before hand

1. k6 run .\scripts\loadTestingScript.js      

