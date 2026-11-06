<div align="center">

  <img src="static/images/logo-icon.svg" alt="TraceBack AI Logo" width="80" height="80">

  # TraceBack AI
  ### Smart Lost & Found Recovery Network
  **"More Than Lost & Found — A Smarter Way to Recover."**

  <p align="center">
    <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.12" />
    <img src="https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django 5.0" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
    <img src="https://img.shields.io/badge/Google_Maps-API%20Verified-4285F4?style=for-the-badge&logo=google-maps&logoColor=white" alt="Google Maps" />
    <img src="https://img.shields.io/badge/Leaflet-JS-199900?style=for-the-badge&logo=leaflet&logoColor=white" alt="Leaflet" />
    <img src="https://img.shields.io/badge/Status-Live%20Ready-success?style=for-the-badge" alt="Status" />
  </p>

  <p align="center">
    <strong>An AI-powered, cryptographic custody and multimodal lost & found recovery ecosystem tailored for university campuses, public transit systems, and institutional help desks.</strong>
  </p>

  <p align="center">
    <a href="#-quick-start--local-setup">Quick Start</a> •
    <a href="#-core-features-breakdown">Features</a> •
    <a href="#-diu-campus-pilot--google-maps-integration">DIU Pilot Map</a> •
    <a href="#-live-deployment-guide">Live Deployment Guide</a> •
    <a href="#-demo-credentials">Demo Accounts</a>
  </p>

</div>

---

## 🌐 Live Application Link

> **Live Deployment URL:**  
> 🔗 **[https://your-traceback-app.onrender.com](https://your-traceback-app.onrender.com)**  
> *(Follow the [Deployment Guide](#-live-deployment-guide) below to link your live hosted application.)*

---

## 📖 Overview & Problem Statement

Every semester across university campuses and transit routes, thousands of valuable belongings—student ID cards, scientific calculators, laptops, umbrellas, and course textbooks—are lost. Previously, students relied on unorganized, noisy social media groups where posts are quickly buried, ownership cannot be verified, and handovers often risk fraud.

**TraceBack AI** solves this with a centralized, enterprise-grade platform:
- 🧠 **Multi-Dimensional AI Matching Engine:** Automatically calculates compatibility scores across 5 dimensions.
- 🛡️ **SecretProof™ Verification:** Prevents unauthorized claims with zero-knowledge private fact checks before custody handover.
- 📍 **Google Maps GPS Integration:** Ground-truth geolocation centered on **Daffodil International University (DIU Ashulia Smart City)**.
- 🏷️ **QR-Coded Custody Passport:** Full digital custody chain-of-custody tracking from intake to claim closure.

---

## 🏫 DIU Campus Pilot & Google Maps Integration

The pilot deployment is configured for **Daffodil International University (Daffodil Smart City, Birulia, Savar/Ashulia)**:

| Landmark Zone | GPS Coordinates (Google Maps Verified) | Facility / Recovery Role |
|---|---|---|
| **Daffodil Smart City (Main Center)** | `23.878870° N, 90.322550° E` | Central Campus Pin (`7MMGV8HF+G2`) |
| **DIU Central Library** | `23.878400° N, 90.322100° E` | 2nd & 3rd Floor study desks; Official Lost & Found Custody Desk |
| **Academic Complex (AB 1-4)** | `23.878315° N, 90.322056° E` | CSE, EEE labs, lecture halls & study lounges |
| **Knowledge Tower** | `23.876841° N, 90.319979° E` | Administrative headquarters, admission center, dean offices |
| **DIU Central Cafeteria & Food Court** | `23.875130° N, 90.321442° E` | Student dining hall, indoor seating, refreshment kiosks |
| **Daffodil Lake & Savora Pavilion** | `23.875953° N, 90.322986° E` | Lakeside walkway, student kiosks, open recreational zone |
| **DIU Sports Ground & Basketball Arena** | `23.875576° N, 90.321080° E` | Central playground, sports court, student pavilion |
| **Shuttle Depot & Student Bus Stand** | `23.875467° N, 90.321835° E` | Gate 1 transit depot connecting Mirpur, Uttara & Dhanmondi |
| **Motorcycle & Bicycle Parking Bay** | `23.875700° N, 90.320500° E` | Student two-wheeler parking facility near Main Gate 1 |

---

## 🚀 Core Features Breakdown

```
TraceBack AI Core Engine
 ├── 1. Lost Item Reporting (Rich Form + SecretProof™)
 ├── 2. Found Item Reporting (Custody Integration)
 ├── 3. AI Multidimensional Matching Engine (0-100% Weighted Scoring)
 ├── 4. AI Image Auto-Categorization & Vision Heuristics
 ├── 5. Interactive Campus Map (Google Maps Tiles + Satellite Hybrid)
 ├── 6. Automatic Match Push Notifications
 ├── 7. SecretProof™ Cryptographic Ownership Verification
 ├── 8. QR-Based Custody Passport & Audit Trail
 ├── 9. JourneyTrace™ Public Transit Recovery (Bus/Train/Metro)
 ├── 10. Bangla & English Voice Input Reporting
 ├── 11. Image SHA-256 Hash Fraud & Velocity Moderation
 ├── 12. Privacy-Safe Shielded In-App Messaging
 └── 13. Interactive Recovery Analytics Dashboard (Chart.js)
```

### 🧠 The AI Matching Engine Formula
$$Confidence = (W_{cat} \times S_{cat}) + (W_{brand} \times S_{brand}) + (W_{nlp} \times S_{nlp}) + (W_{geo} \times S_{geo}) + (W_{time} \times S_{time})$$

- **Category Match ($25\%$):** Exact tree hierarchy alignment.
- **Brand & Color ($20\%$):** Normalized attribute token similarity.
- **NLP Text Semantics ($25\%$):** Tokenized intersection of description details.
- **Haversine Distance Proximity ($15\%$):** Proximity score within 150m – 5km campus radius.
- **Temporal Delta ($15\%$):** Time-window score based on incident date/time difference.

---

## 👥 Demo Credentials

The platform comes pre-seeded with authenticated demo accounts for every operational role:

| Role | Username | Password | Access Level |
|---|---|---|---|
| **System Administrator** | `admin` | `admin123` | Django Admin, Fraud Review Center, Platform Metrics |
| **Desk Staff Officer** | `desk_officer` | `staff123` | DIU Library Desk, QR Custody Manager, Verification Handover |
| **Student Seeker** | `diu_student` | `student123` | Lost item reports, active AI matches, private messaging |
| **Finder Student** | `tanvir_finder` | `finder123` | Found item reports, custody deposit requests |
| **Transit Authority** | `railway_staff` | `transport123` | DIU Campus Shuttle & Transit recovery section |

---

## 💻 Quick Start & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/traceback_ai.git
cd traceback_ai
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Database
```bash
python manage.py migrate
python seed_data.py
```

### 5. Launch Development Server
```bash
python manage.py runserver
```
Visit **http://127.0.0.1:8000/** in your browser.

---

## 🚀 Live Deployment Guide

Deploy your TraceBack AI instance live in less than 5 minutes on **Render.com** (Free Tier):

### Option A: Deploy to Render.com (Recommended)

1. **Push your code to GitHub** (see Git steps below).
2. Go to [Render.com](https://render.com) and click **"New +" &rarr; "Web Service"**.
3. Select your GitHub repository.
4. Configure the settings:
   - **Name:** `traceback-ai`
   - **Region:** Singapore / Frankfurt
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn traceback_bd.wsgi:application`
5. Click **"Create Web Service"**.
6. Render will automatically install dependencies, collect static files, run migrations, seed DIU data, and launch your live URL!

### Option B: Deploy to PythonAnywhere

1. Create a free account on [PythonAnywhere](https://www.pythonanywhere.com/).
2. Open a Bash console and clone your repo:
   ```bash
   git clone https://github.com/your-username/traceback_ai.git
   ```
3. Set up virtualenv and install `requirements.txt`.
4. In the **Web** tab, set WSGI file to point to `traceback_bd/wsgi.py` and specify your virtualenv path.
5. Reload web app.

---

## 📁 Project Structure

```
traceback_bd/
├── accounts/               # Custom user model, RBAC, profiles, registration
├── core/                   # Home feed, Google Maps interactive campus view, analytics
├── items/                  # Lost & Found reporting, SecretProof™, voice recognition
├── matching/               # Multimodal AI similarity scoring engine
├── custody/                # QR custody generator, inventory lockers, audit logs
├── communication/          # Privacy-shielded in-app buyer/finder messaging
├── media/                  # Real student item photos (ID card, books, flask, keys)
├── static/                 # Brand SVG logos, CSS, JavaScript utilities
├── templates/              # Tailored responsive Django HTML templates
├── traceback_bd/           # Project settings, WSGI, URLs, WhiteNoise configuration
├── build.sh                # Production cloud build & migration script
├── Procfile                # Gunicorn process definition
├── requirements.txt        # Production dependency manifest
├── seed_data.py            # Automated DIU campus items and demo users seeder
└── manage.py               # Django management CLI
```

---

## 📄 License & Credits

Distributed under the **MIT License**. Developed for modern educational and public transit institutions to centralize and secure lost item recoveries.
