# Project-Planetary-Defense-Playground
[![Python 3.13.6](https://img.shields.io/badge/python-3.13.6-blue.svg)](https://www.python.org/downloads/release/python-3136/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) ![Teamwork](https://img.shields.io/badge/Teamwork-Collaboration-success?style=flat&logo=github)

## Project Overview
**Our project, Planetary Defense Playground, is an interactive asteroid impact simulation platform. It helps users model and visualize potential asteroid threats and mitigation strategies using real NASA and USGS data.** 

> Our Project, **Project-Planetary-Defense-Playground**, helps user  model and visualize potential asteroid threats and mitigation strategies that using **real Nasa Data**. The simulation utilizes Nasa's open asteroid datasets and impact monitoring APIs to preditct data into clear, visual forms. The Project mixes **science with interactivity** to raise awareness about planetary defense for educators, students, and space enthusiasts.

---

## Features and Functionality
Our Project Provides a three stage workflow (Discovery, Assessment, Mitigation) to simulate a real-world response to a Asteroid threat.

**Key Features:**
1. Real Time threat Detection:
     - Displays a prominent "critical" banner and "breaking news" alert upon detection of threat.
     - Presents Comprehensive data on the asteroid's size, speed, and trajectory.
2. Quantative Risk Assessment:
     - Calculates and visualizes impact severity metrics, including impact probabilty, potential casualities, etc.
3. Interactive Mitigation Simulation:
    - Allows the user to select from three defense protocols: **Survey Mission**, **Deflection Protocol**, or **Evaluation Plan**.
    - Instantly displays the rist assessment to demonstrate the effectiveness of the chosen action4. .
4. Mission Timeline:
   - Provides a clear, step-by-step overview of the response: **Discovery**, **RIsk Assessment**, **Mitigation Action**, and **Final Outcome**.

---

  ## Tech Stack
  - **Back-end/Simulation:** Python, FastAPI
  - **Data/Notebooks:** Google Colab
  - **Front-end/UI:** HTML, CSS, JS
  - **Data Source:** NASA Near-Earth Object (NEO) Web Service Application Programming Interface (API), U.S. Geological Survey (USGS) National Earthquake Information Center (NEIC) Earthquake Catalog, Small-Body Database Query Tool

---

## Setup and Local Installation
Follow these steps to run a local copy of the project:

1.  **Clone the Repository:**
    '''bash
    git clone https://github.com/Team-Orbitosaurs/Project-Planetary-Defense-Playground
    cd Project-Planetary-Defense-Playground
    '''

2. **Install Dependencies:**
    '''bash
    #Assuming you used Python requirements
    pip install -r requirements.txt
     '''

3. **Configure API Key (Crucial Step):**
    * Create a file named .env in the root directory.
    * Obtain your API Key from (api.nasa.gov).
    * Add the key to your .env file in this format:
        API_KEY="[YOUR_KEY_HERE]

4.  **Run the Application:**
    bash
    # Use the specific command for your Python/JS backend
    uvicorn --reload --port 5000
    
    The application should now be available at http://localhost:5000.

---

## 👨‍💻 Team Orbitosaurs
This project was built by the following team members:

1. [Haffi Ansari](https://github.com/Haffi-Ansari)
2. [Usman Amjad](https://github.com/usmanamjad7)
3. [Hadiqa Siddique](https://github.com/hadiqasiddique)
4. [Ayesha Aftab](https://github.com/aayeshaaftab2005-rgb)
5. [Hadi Ansari](https://github.com/HadiAnsari1)
6. [Shahzaib Kazmi](https://github.com/shahzaibkazmi30)
   
---

## 🌟 Future Improvements
Given more time, we would focus on:
