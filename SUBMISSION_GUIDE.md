# Task 11: Submission Assembly & Documentation Guide

This guide walks you through compiling your final submission for **Task 11: Full Application Containerization (L&T EduTech)**, whether you are submitting as a **PDF Document** or a **Public GitHub Repository**.

---

## Part A: Compiling the Final Submission PDF

Most evaluations require visual proof of functionality, container health, and architecture. Follow this step-by-step checklist to gather your screenshots:

### Screenshot 1: Directory Structure Verification
- **Command:**
  ```bash
  # In PowerShell or VS Code Terminal:
  tree /F /A
  # or
  Get-ChildItem -Recurse | Select-Object FullName
  ```
- **What to capture:** Clean view showing `backend/`, `frontend/`, `docker-compose.yml`, and documentation files.
- **Label in PDF:** `Figure 1: Project Directory Structure and Modular Organization`.

### Screenshot 2: Docker Build and Container Orchestration
- **Command:**
  ```bash
  docker compose up -d --build
  ```
- **Followed by:**
  ```bash
  docker compose ps
  ```
- **What to capture:** The terminal showing both `dl-backend-api` and `dl-frontend-ui` in state `Up (healthy)`.
- **Label in PDF:** `Figure 2: Docker Compose Multi-Container Orchestration and Health Status`.

### Screenshot 3: Backend API Validation & cURL Output
- **Command:**
  ```bash
  # Check health
  curl -i http://localhost:5000/health

  # Check inference
  curl -i -X POST http://localhost:5000/predict ^
       -H "Content-Type: application/json" ^
       -d "{\"inputs\": [0.55, 1.20, -0.42, 0.88, 2.15]}"
  ```
- **What to capture:** HTTP 200 responses showing status, latency, and prediction dictionary.
- **Label in PDF:** `Figure 3: Flask Backend API Health & Prediction Endpoint Verification`.

### Screenshot 4: Automated Test Suite Output
- **Command:**
  ```bash
  python test_endpoints.py
  ```
- **What to capture:** Terminal output displaying `8 PASSED | 0 FAILED` and the latency benchmarks.
- **Label in PDF:** `Figure 4: Automated Endpoint Verification and Performance Benchmark Results`.

### Screenshot 5: Streamlit UI Frontend in Browser
- **URL:** Open `http://localhost:8501` in your browser.
- **Actions before taking screenshot:**
  1. Ensure the sidebar displays `🟢 Backend API: Healthy & Connected`.
  2. Select a preset (e.g., *Profile A: Normal Component*) or enter custom values.
  3. Click **Submit Inference Request to Flask API**.
- **What to capture:** Full browser window showing the metrics cards (Predicted Class, Confidence, Latency), the Softmax probability distribution bar chart, and the expandable JSON audit view.
- **Label in PDF:** `Figure 5: Streamlit Interactive Frontend Model Consumption Dashboard`.

### Recommended Document Outline for Final PDF:
1. **Title Page:** Candidate Name, Roll / Registration Number, Task 11 Title.
2. **Architecture Overview:** Mermaid.js diagram showing User $\rightarrow$ Streamlit $\rightarrow$ Docker Network $\rightarrow$ Flask API $\rightarrow$ DL Model.
3. **Directory Structure & Configurations:** Code snippets of `docker-compose.yml` and both Dockerfiles.
4. **Verification Screenshots:** Figures 1 through 5 with captions.
5. **Testing Report:** Include the sections from `TESTING_REPORT.md` (Functionality, Integration Quality, Deployment Readiness, Observations).

---

## Part B: Submitting via Public GitHub Repository

If submitting a GitHub URL:

### 1. Initialize and Push to GitHub
```bash
git init
git add .
git commit -m "feat: complete Task 11 full application containerization"
git branch -M main
git remote add origin https://github.com/<your-username>/flask-dl-containerization.git
git push -u origin main
```

### 2. Verify Repository Contents
Make sure the following key files are present in the root:
- `README.md` (already configured with full architecture and execution steps)
- `docker-compose.yml`
- `backend/`
- `frontend/`
- `TESTING_REPORT.md`
- `SUBMISSION_GUIDE.md`
