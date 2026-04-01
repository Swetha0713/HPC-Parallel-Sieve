# 🚀 HPC Parallel Sieve Cluster
A High-Performance Computing (HPC) dashboard designed to analyze hardware scalability using the Segmented Sieve of Eratosthenes.

## 🔬 Project Overview
This project implements a **Manager-Worker architecture** to discover prime numbers across multiple CPU cores. It serves as a performance laboratory to validate:
* **Amdahl's Law:** Fixed workload speedup limits.
* **Gustafson's Law:** Scaled workload efficiency.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Parallelism:** `multiprocessing` (Process Pool)
* **UI/UX:** Streamlit
* **Analytics:** Pandas & Matplotlib

## 📈 Key HPC Insights
* **Data Decomposition:** The search range is partitioned into independent segments to maximize L1/L2 cache locality.
* **Serial Bottleneck:** Identifies the $O(\sqrt{N})$ serial pre-computation as the primary scaling limit ($s$).
* **Efficiency Tracking:** Real-time calculation of Parallel Efficiency and Speedup ratios.

## 🚀 How to Run Locally
1. Clone the repo: `git clone <your-repo-link>`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch Dashboard: `streamlit run app.py`