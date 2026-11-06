# 🔍 TraceBack AI — Smart Lost & Found Recovery Network
> **"More Than Lost & Found — A Smarter Way to Recover."**

[![Django Version](https://img.shields.io/badge/Django-5.0.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python Version](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Frontend](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Mapping](https://img.shields.io/badge/Google_Maps_&_Leaflet-1.9.4-4285F4?style=for-the-badge&logo=google-maps&logoColor=white)](https://leafletjs.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![DIU Pilot](https://img.shields.io/badge/Pilot_Campus-DIU_Smart_City-0891b2?style=for-the-badge&logo=google-scholar&logoColor=white)](https://daffodilvarsity.edu.bd/)

---

## 📌 Overview

Every day across university campuses, transit routes, and public facilities, thousands of valuable belongings—smartphones, laptops, institutional smart ID cards, textbooks, keys, and water flasks—are misplaced. Traditional recovery relies on chaotic social media posts and unstructured noticeboards with high rates of fraudulent claims.

**TraceBack AI** is an intelligent, full-stack lost-and-found ecosystem built with **Django**, **Tailwind CSS**, and **Leaflet.js/Google Maps**. It bridges the gap between seekers, finders, and institutional custody desks through multi-criteria AI matching, cryptographic **SecretProof™** verification, automated QR custody chains, and real-time transit recovery.

The initial flagship pilot is custom-calibrated for **Daffodil International University (DIU Ashulia Smart City)**, with GPS-mapped campus landmarks and verified custody desks.

---

## 🏛️ Pilot Campus: Daffodil International University (DIU)

TraceBack AI is integrated with physical coordinates and verified building zones of **Daffodil Smart City (Birulia, Savar / Ashulia, Dhaka)**:

| Landmark Zone | GPS Coordinates (Google Maps Verified) | Facilities & Function |
|---|---|---|
| **Daffodil Smart City (Main Center)** | `23.87887° N, 90.32255° E` | Central university campus pin & campus radius |
| **Academic Complex (AB 1-4 & CSE Labs)** | `23.878315, 90.322056` | CSE, EEE, SE lecture galleries and hardware labs |
| **DIU Central Library & Study Commons** | `23.878400, 90.322100` | 2nd & 3rd floor reading desks; Official Custody Desk |
| **Knowledge Tower (Administrative HQ)** | `23.876841, 90.319979` | Executive offices, admission center & security desk |
| **Central Cafeteria & Food Court Area** | `23.875130, 90.321442` | Student dining pavilion, indoor canteen & kiosks |
| **Daffodil Lake & Savora Pavilion** | `23.875953, 90.322986` | Lakeside walkway, student kiosks & seating area |
| **Basketball Ground & Sports Arena** | `23.875576, 90.321080` | Central basketball court, sports pavilion |
| **DIU Transport Depot & Shuttle Bay** | `23.875467, 90.321835` | Main Gate 1 on Khagan Road, Mirpur/Uttara shuttles |
| **Student Parking Bay** | `23.875700, 90.320500` | Two-wheeler & bicycle parking lot near Main Gate |

---

## ⚡ Core Architecture & 13 Flagship Features

```
+-----------------------------------------------------------------------------------+
|                                  TraceBack AI                                     |
|                       Smart Campus Lost & Found Pipeline                          |
+-----------------------------------------------------------------------------------+
       |                                       |                               |
[Seeker Reports Lost]                  [Finder Reports Found]           [Transit Recovery]
       |                                       |                               |
       +-------------------> [ AI Multimodal Match Engine ] <------------------+
                                  | (Score 0-100%)
                                  v
                       [ Threshold > 50% Match ]
                                  |
                                  v
                     [ Anonymous Shielded Messaging ]
                                  |
                                  v
                      [ SecretProof™ Verification ]
                                  |
                                  v
                     [ Institutional QR Custody Desk ]
                                  |
                                  v
                        [ Verified Handover & Closure ]
```

1. **Feature 1: Lost Item Reporting**
   - Captures item category, brand, primary color, date, time, location, safe public area, description, and confidential ownership proofs.
2. **Feature 2: Found Item Reporting & Drop-Off**
   - Allows students and citizens to log discovered belongings and assign them directly to campus lost-and-found desks.
3. **Feature 3: AI Smart Multi-Dimensional Matching Engine**
   - Weighted algorithmic matching combining:
     - **Category Match:** 25%
     - **NLP Description Semantic Token Overlap:** 25%
     - **Brand & Color Similarity:** 20%
     - **Haversine Geospatial Distance Proximity:** 15%
     - **Temporal Window Delta:** 15%
4. **Feature 4: AI Image Recognition & Auto-Categorization**
   - Automated category recommendation based on image metadata, filename tokens, and visual keywords.
5. **Feature 5: Interactive Campus Recovery Map**
   - Real **Google Maps Roadmap** & **Google Satellite Hybrid** layers inside Leaflet.js.
   - Exact DIU building landmarks, approximate 150m privacy radius circles, and one-click zone fly-to buttons.
   - Direct *"Open in Google Maps ↗"* verification links on every popup.
6. **Feature 6: Automated Match Notifications**
   - Real-time in-app alerts dispatched whenever an AI match crosses the 50% confidence threshold.
7. **Feature 7: SecretProof™ — Fraud-Proof Ownership Verification**
   - Solves fraudulent claims. Genuine owners provide secret, hidden facts (serial number suffix, internal engraving, lockscreen wallpaper, private tear). Only authorized desk officers inspect proofs before approving handover.
8. **Feature 8: QR-Based Custody Passport & Tracking**
   - Dynamic QR code generation for every item deposited at campus desks.
   - Comprehensive audit trail: `Deposited` → `Stored in Locker/Shelf` → `Owner Verified` → `Handover Completed`.
9. **Feature 9: JourneyTrace™ — Transit Recovery System**
   - Dedicated public & university shuttle recovery (Bus, Train, Metro Rail).
   - Tracks vehicle fleet number, route, boarding & drop-off stops, and seat/compartment numbers.
10. **Feature 10: Bangla & English Voice Reporting**
    - Built-in Web Speech API (`webkitSpeechRecognition`) supporting real-time voice input in both **Bangla (`bn-BD`)** and **English (`en-US`)**.
11. **Feature 11: Fraud Detection & Image Hash Matching**
    - SHA-256 duplicate image fingerprinting, rate-limiting velocity monitors, and an administrative moderation review center.
12. **Feature 12: Privacy-Safe Shielded Messaging**
    - Anonymous end-to-end in-app chat between seekers and finders using handles (e.g. *Seeker #482*, *Finder #917*) without exposing personal phone numbers or email addresses.
13. **Feature 13: Recovery Analytics Dashboard**
    - Visual Chart.js metrics detailing recovery success rates, category breakdowns, pipeline status distributions, and area report density.

---

## 👥 Pre-Configured Demo Accounts

All accounts are pre-seeded with genuine student items, matches, and QR custody records:

| Role | Username | Password | Assigned Function |
|---|---|---|---|
| **System Administrator** | `admin` | `admin123` | Full access to Django admin, moderation center, fraud flags |
| **DIU Desk Officer** | `desk_officer` | `staff123` | Manages DIU Central Library Desk, QR scanner, handover execution |
| **Student Seeker** | `diu_student` | `student123` | Seeker with open lost reports, active matches, and chat threads |
| **Student Finder** | `tanvir_finder` | `finder123` | Reported found items deposited at library and cafeteria |
| **Transit Authority** | `railway_staff` | `transport123` | DIU shuttle fleet & transit route custody manager |

---

## 💻 Local Quickstart

### Prerequisites
- Python 3.10+ (Recommended: Python 3.12)
- Git
- pip

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/traceback_bd.git
cd traceback_bd

# 2. Create and activate a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Populate authentic DIU student belongings & AI matches
python seed_data.py

# 6. Start the local development server
python manage.py runserver
```

Open your browser and navigate to:
- **Application:** `http://127.0.0.1:8000/`
- **DIU Campus Map:** `http://127.0.0.1:8000/map/`
- **Admin Portal:** `http://127.0.0.1:8000/admin/`

---

## 🌐 1-Click Live Deployment Guide

TraceBack AI is production-ready with pre-configured `Procfile`, `build.sh`, `runtime.txt`, `whitenoise` static serving, and dynamic host permissions.

### Option A: Deploy on Render (Recommended - Free)

1. Fork or push this repository to your **GitHub** account.
2. Sign in to [Render.com](https://render.com) using your GitHub account.
3. Click **New +** → **Web Service**.
4. Select your `traceback_bd` repository.
5. Fill in the deployment settings:
   - **Name:** `traceback-ai` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** `Singapore` (fastest for Bangladesh) or `Frankfurt`
   - **Branch:** `main`
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn traceback_bd.wsgi:application`
6. Click **Create Web Service**.
7. Render will automatically build the app, run migrations, seed sample data, and give you a live URL:  
   `https://traceback-ai.onrender.com`

### Option B: Deploy on Railway

1. Sign in to [Railway.app](https://railway.app).
2. Click **New Project** → **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will automatically detect the `Procfile` and deploy the service.
5. In project settings, generate a domain.

---

## 📁 Project Directory Structure

```
traceback_bd/
|-- accounts/               # User authentication, custom User model, roles, profiles
|-- core/                   # Home, DIU Campus Map, Analytics, static informational views
|-- items/                  # Lost & found reporting, categories, item detail, speech input
|-- matching/               # Multimodal AI similarity engine, MatchRecord, notifications
|-- custody/                # Institutional desks, QR code generation, custody audit logs
|-- communication/          # Privacy-safe shielded messaging threads & inbox
|-- templates/              # Tailwind CSS HTML templates (Mid Cyan & Off-White theme)
|   |-- base.html           # Responsive navbar, user avatar, mobile navigation drawer
|   |-- core/               # index.html, map.html (Google Maps + Leaflet), analytics.html
|   |-- items/              # report_lost.html, report_found.html, item_detail.html
|   |-- custody/            # qr_scan.html, custody_passport.html, desk_list.html
|-- static/                 # Stylesheet, custom SVG logos, client-side scripts
|-- media/                  # Real student item photographs, QR custody passports
|-- traceback_bd/           # Django settings, WSGI/ASGI configurations, root URLs
|-- build.sh                # Automated Linux build script for Render/Railway deployment
|-- Procfile                # Gunicorn web server process configuration
|-- runtime.txt             # Python runtime specification
|-- requirements.txt        # Production Python dependencies
|-- seed_data.py            # Automated database seeder with DIU student belongings
`-- manage.py               # Django CLI management entrypoint
```

---

## 🎨 Color Palette & Visual Theme

| Token | Hex Value | Usage |
|---|---|---|
| **Primary Cyan** | `#0891b2` | Core branding, primary action buttons, active states |
| **Deep Cyan** | `#0e7490` | Headings, hero badges, building icons |
| **Light Cyan Accent** | `#ecfeff` | Card highlights, badge backgrounds |
| **Off-White Surface** | `#f8fafc` | Main application background, canvas surfaces |
| **Crisp White** | `#ffffff` | Floating cards, modals, navigation containers |
| **Alert Rose** | `#e11d48` | Lost item status pills, high-priority alert badges |
| **Success Emerald** | `#059669` | Successfully recovered badges, custody confirmations |

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

<div align="center">
  <b>Developed for Daffodil International University (DIU) Smart City &amp; Campus Recovery Network</b><br>
  <sub>Powered by Django 5 &bull; Leaflet.js &bull; Google Maps &bull; Tailwind CSS</sub>
</div>
