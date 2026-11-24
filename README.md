# Server Monitoring Dashboard

## Overview
Server Monitoring Dashboard is a Python-based system monitoring project that displays CPU utilization, memory utilization, disk utilization, system uptime and system information through a web-based dashboard.

## Features
- Live CPU monitoring
- RAM usage monitoring
- Disk usage monitoring
- System uptime
- Resource threshold alerts
- CPU performance graph
- CSV monitoring history
- Browser-based dashboard

## Technologies Used
- Python
- HTML
- CSS
- JavaScript
- CSV
- Git
- GitHub

## Architecture

Python backend collects system metrics.
The backend serves the dashboard and metrics through HTTP.
The frontend requests metrics and displays them.
Monitoring readings are stored in a CSV file.

## How to Run

1. Install Python.
2. Clone or download this repository.
3. Open the project folder.
4. Run:

   python server.py

5. Open http://localhost:8000 in your browser.

## Project Structure

server-monitoring-dashboard/
- server.py
- dashboard.html
- monitoring_log.csv
- README.md
- .gitignore

## Future Improvements
- Email notifications
- Multiple server monitoring
- Docker deployment
- Cloud deployment
- More performance graphs
- Git pull demonstrate: remote update.
- Feature branch: alert development demonstration.
