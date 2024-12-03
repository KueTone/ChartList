

# ChartList  
**A Craigslist Clone**


## Backend Setup  

### 1. Install Dependencies  
Navigate to the backend folder and run:  
```bash
pip install -r requirements.txt
```

### 2. Create `.env` File  
In the `backend` folder, create a `.env` file with the following content:  
```env
HOST=127.0.0.1
PORT=8000
LOCATION=us-central1

DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_NAME=craigslist
```

### 3. Export Google Application Credentials  
Download your Google JSON credentials file and place it in the `backend` folder.

#### On macOS or Linux:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/absolute/path/to/your-service-account-key.json"
```

#### On Windows PowerShell:
```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\absolute\path\to\your-service-account-key.json"
```

---

## Running the Servers  

### 1. Start the Backend  
From the `backend` folder, run:  
```bash
python backend.py
```

### 2. Install Frontend Dependencies  
Navigate to the `frontend` folder and run:  
```bash
npm install
```

### 3. Start the Frontend  
In the `frontend` folder, start the server with:  
```bash
npm start
```