# Real-time-Weather-Data-Visualizer
An interactive weather dashboard built using Dash by Plotly that fetches live weather data from the OpenWeather API for multiple cities.

This tool allows users to:
-	Search and add any city worldwide
-	View current weather conditions (temperature, humidity, wind speed, description)
-	Explore 5-day forecast trends with interactive line and bar charts
-	Compare weather conditions across cities
-	Toggle between Light 🌞 and Dark 🌙 modes
-	View condition distribution per city with pie charts

---

## 📸 Features Preview
- 🔎 Search any city and view live data
- 🌍 Multi-city comparison
- 📈 Interactive line & bar charts
- 🥧 Condition distribution pie charts
- 🌞🌙 Theme toggle

---

## 📊 Data Overview
- **Source**: OpenWeather API
- **Data**: Live updates (current snapshot + 5-day/3-hour forecast)
- **Metrics Captured**:
  - `Temperature` (°C)
  - `Humidity` (%)
  - `Wind Speed` (km/h)
  - `Weather Condition` (Clear, Rain, Clouds, etc.)
 
---

## ⚙️ Installation & Setup

🔁 Clone this Repository
```bash
git clone https://github.com/JagguDada01/Real-time-Weather-Data-Visualizer.git
cd Real-time-Weather-Data-Visualizer
```
📦 Create Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
🔧 Install Dependencies
```bash
pip install -r requirements.txt
```
▶️ Run the Application
```bash
python weather.py
```
🌐 Then open your browser and visit:
```
http://127.0.0.1:8050
```
---
## ❗ Trouble? Port Already in Use?

**If you see this error when running the app:**
- Address already in use
- Port 8050 is in use by another program.

✅ Kill the process using port 8050

💻 On macOS/Linux:
```bash
lsof -i :8050
kill -9 <PID>
```
Replace `<PID>` with the number shown in the output of the lsof command.

🖥️ On Windows (Command Prompt):
```bash
netstat -ano | findstr :8050
```
- This will show something like:- **TCP    127.0.0.1:8050   ...   PID: 12345**

**Then stop the process using:**
```bash
taskkill /PID 12345 /F
```
- Replace 12345 with the actual Process ID (PID) shown.


