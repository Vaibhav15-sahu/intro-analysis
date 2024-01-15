# Django Video Introduction Analysis

This Django application allows users to record video introductions, analyzes facial expressions, monitors tab switching, extracts keywords, and generates a comprehensive report.

## Table of Contents
- [Installation](#installation)
- [Run](#Run)
- [Requirements](#requirements)
- [Approach](#approach)
  - [Facial Expression Analysis](#facial-expression-analysis)
  - [Keyword Extraction](#keyword-extraction)

## Installation
1. Clone the repository:
2. Create directory:
    ```bash
    cd your-repository
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
## Run
1. Run the Django migrations:
    ```bash
    python manage.py migrate
2. Start the development server:
    ```bash
    python manage.py runserver
## Reqirements
    

1. Django
2. OpenCV
3. MySql
4. FER (Facial Expression Recognition)
5. AssemblyAI
6. Spacy

## Approach
### Expression Analysis
The facial expression analysis is implemented using the FER module, which leverages OpenCV for video frame processing and emotion detection. The frames are converted to grayscale and then analyzed for facial expressions. The unique detected emotions are recorded, and the results are stored in the database.

### Keyword Extraction
Keyword extraction is performed using the spaCy library. The transcribed text from the user's audio is processed to identify entities such as names, organizations, and hobbies. The extracted information is stored in the database.
For detailed information on the implementation, refer to the code comments and documentation within the application.