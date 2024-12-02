# ChartList
Craigslist Clone

# ChartList
Craigslist Clone


# How to get started (OLD)

git:
git clone 
git checkout main

## Backend Install Dependencies
Run in backend folder
```pip install -r requirements.txt```

## Backend Run
Run in backend folder
```python backend.py```

Make a .env file. this will hold your important stuff
### making .env
```
HOST=127.0.0.1
PORT=8000
LOCATION=us-central1

//For FastAPI
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_NAME=craigslist
```
### export Credentials
In the terminal rooted in your backend, download your Google JSON credentials file and place it there
then run this command:
```
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your-service-account-key.json"
```

### Start servers
```
cd backend
python backend.py
cd ..
cd frontend
npm install
npm run dev
```