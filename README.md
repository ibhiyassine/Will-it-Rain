# Will-It-Rain Project

This project is a web application with a Nuxt.js frontend and a Python FastAPI backend.

## Project Structure

- `/frontend`: Contains the Nuxt.js frontend application.
- `/backend`: Contains the Python FastAPI backend application and its virtual environment.

## Getting Started

Follow the instructions below to set up and run both the frontend and backend services.

### Frontend (Nuxt.js)

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    Make sure you have Node.js and npm installed. Then, run the following command to install the project's dependencies.
    ```bash
    npm install
    ```

3.  **Run the development server:**
    This command will start the Nuxt.js development server, typically on `http://localhost:3000`.
    ```bash
    npm run dev
    ```

### Backend (FastAPI)

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv ./
    ```

3.  **Activate the virtual environment:**
    The project includes a pre-configured virtual environment. Activate it using the appropriate script for your shell.
    
    For Bash/Zsh:
    ```bash
    source bin/activate
    ```
    
    For Fish:
    ```bash
    source bin/activate.fish
    ```

    For Windows (Command Prompt/PowerShell):
    ```bash
    .\bin\Activate.ps1
    ```

5.  **Install Python packages:**
    Install all the required packages using the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

6.  **Run the FastAPI server:**
    Navigate to the `src` directory and start the Uvicorn server. The API will be available at `http://localhost:8000`.
    ```bash
    cd src
    uvicorn apiEndpoint:app --reload
    ```

## Usage

Once both the frontend and backend servers are running, you can access the web application by opening your browser and navigating to the frontend URL (e.g., `http://localhost:3000`).
