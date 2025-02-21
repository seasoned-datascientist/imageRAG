**Multi-Modal Retrieval System**

Description:
This project is a Multi-Modal Retrieval System that combines natural language processing (NLP)and image processing models to retrieve images that best match a user's descriptive query.Futhermore, the user is also able insert photos of their own into the system and the system returns top k similar photos. 

![multimodal](https://github.com/user-attachments/assets/b2c6c17e-49b1-4598-ada3-c65e252f148b)

**Installation**

Prerequisites:
Ensure you have the following installed:
Python 3.8+
pip
Virtual environment (optional but recommended)
Node.js (for frontend)

**Tools**
Faiss
Clip
Flask

**Set up a virtual environment and install dependencies:**
   pip install -r requirements.txt
   
  **Navigate to the frontend directory and install dependencies:**
  
  cd frontend
  npm install

**Running the System:**

Backend:
Start the backend server:
cd backend
python app.py

Frontend:
Start the frontend server:
cd frontend
npm start

The application will be accessible at `http://localhost:3000`.

![PHOTO-2025-02-20-17-43-58](https://github.com/user-attachments/assets/787edfe0-0fc2-4920-898d-4fb03418de3a)

**Running Tests**
To run unit tests for the backend:
pytest tests/

To run frontend tests:
cd frontend
npm test

**Assumptions:**
The image dataset is pre-indexed using a vector search engine.
The system uses a pre-trained CLIP model for multi-modal retrieval.
The frontend is minimalistic, focused on search and display functionalities.






