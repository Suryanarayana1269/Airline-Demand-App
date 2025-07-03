# ✈️ Airline Demand Insights Dashboard

A modern web app to analyze live airline market demand, trends, and activity using open flight data.  
Built with **FastAPI** (backend), **Streamlit** (frontend), and **Plotly/PyDeck** for interactive visualizations.

---

## 🚀 Features

- **Live Data Fetching:** Scrapes live airline data from OpenSky Network API.
- **Interactive Dashboard:** Filter by country and hour, view charts and maps.
- **Key Insights:**  
  - Top 5 origin countries  
  - Hourly activity  
  - Most active callsigns  
  - Top routes (origin → current location)  
  - Flight origins map  
  - Flight density heatmap  
  - Key stats: total flights, unique aircraft, average flights/hour, peak hour/day
- **Modern UI:** Responsive, emoji-enhanced, and visually appealing.

---

## 🏗️ Project Structure

```
Airline-Demand-App/
│
├── backend/
│   ├── main.py         # FastAPI app
│   ├── scraping.py     # Data fetching from OpenSky
│   ├── processor.py    # Data cleaning/processing
│   └── insights.py     # Insights generation
│
├── frontend/
│   └── app.py          # Streamlit dashboard
│
└── README.md           # Project documentation
```

---

## ⚡ Quick Start

### 1. Clone the repo

```sh
git clone https://github.com/yourusername/airline-demand-app.git
cd airline-demand-app
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```
Or manually:
```sh
pip install fastapi uvicorn requests pandas streamlit plotly pydeck
```

### 3. Run the backend

```sh
cd backend
uvicorn main:app --reload
```
- Backend runs at [http://localhost:8000](http://localhost:8000)

### 4. Run the frontend

Open a new terminal:
```sh
cd frontend
streamlit run app.py
```
- Frontend runs at [http://localhost:8501](http://localhost:8501)

---

## 🖥️ Usage

- Use the sidebar to filter by **Origin Country** and **Hour of Day**.
- Click **Fetch Latest Activity Insights** to update the dashboard.
- Explore charts, tables, maps, and heatmaps for actionable insights.

---

## 📝 Technical Details

- **Data Source:** [OpenSky Network API](https://opensky-network.org/)
- **Backend:** Python, FastAPI, Pandas
- **Frontend:** Streamlit, Plotly, PyDeck
- **Deployment:** Local (see above), can be deployed to cloud/VM/Streamlit Cloud

---

## 📦 API Endpoints

- `GET /fetch?country=...&hour=...`  
  Returns processed insights as JSON.
- `GET /fetch?all_options=true`  
  Returns available filter options.

---

## 🛠️ Customization

- To use a different data source, update `backend/scraping.py`.
- To add more insights, edit `backend/insights.py` and update the frontend accordingly.

---

## 🙋 FAQ

- **Why do routes show coordinates?**  
  OpenSky API does not provide true destination data; routes are shown as "Origin → [lat, lon]".

- **Can I deploy this online?**  
  Yes! Use Streamlit Cloud, Heroku, or any VM with Python.

---

## 👤 Author

Made with ❤️ by Suryanarayana

---

## 📄 License

MIT License (add your preferred license here)
