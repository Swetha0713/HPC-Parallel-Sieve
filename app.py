import streamlit as st
import multiprocessing
import time
import math
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. COMPUTATIONAL CORE ---
def get_base_primes(limit):
    """Serial Phase: Found by 1 core (The 's' in Amdahl's Law)."""
    sieve = [True] * (limit + 1)
    for p in range(2, int(math.sqrt(limit)) + 1):
        if sieve[p]:
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
    return [p for p in range(2, limit + 1) if sieve[p]]

def sieve_segment(start, end, base_primes):
    """Parallel Phase: Worker nodes process these segments."""
    size = end - start
    segment = [True] * size
    for p in base_primes:
        first_multiple = (start + p - 1) // p * p
        if first_multiple < p * p: first_multiple = p * p
        for j in range(max(first_multiple, p * p), end, p):
            segment[j - start] = False
    return sum(1 for is_prime in segment if is_prime)

# --- 2. HPC MANAGER ---
def run_hpc_job(N, num_procs):
    start_time = time.perf_counter()
    sqrt_n = int(math.sqrt(N))
    
    # Serial part
    t_s_start = time.perf_counter()
    base_primes = get_base_primes(sqrt_n)
    t_serial = time.perf_counter() - t_s_start
    
    # Data Decomposition
    chunk_size = (N - sqrt_n) // num_procs
    tasks = []
    for i in range(num_procs):
        s = sqrt_n + 1 + (i * chunk_size)
        e = s + chunk_size if i < num_procs - 1 else N + 1
        tasks.append((s, e, base_primes))
    
    # Parallel Execution
    with multiprocessing.Pool(processes=num_procs) as pool:
        results = pool.starmap(sieve_segment, tasks)
    
    total_time = time.perf_counter() - start_time
    return total_time, t_serial, (len(base_primes) + sum(results))

# --- 3. UI DASHBOARD ---
st.set_page_config(page_title="HPC Prime Lab", layout="wide")
st.title("🚀 HPC Parallel Sieve Cluster")

with st.sidebar:
    st.header("Settings")
    N_val = st.number_input("Problem Size (N)", value=10000000)
    cores = st.multiselect("Test Core Counts", [1, 2, 4, 8], default=[1, 2])
    run = st.button("Launch Experiment")

if run:
    results = []
    for c in cores:
        st.write(f"Testing {c} Core(s)...")
        t_tot, t_ser, count = run_hpc_job(N_val, c)
        results.append({"Cores": c, "Time": t_tot, "Serial": t_ser})
    
    df = pd.DataFrame(results)
    t1 = df['Time'].iloc[0]
    df['Speedup'] = t1 / df['Time']
    df['Efficiency'] = (df['Speedup'] / df['Cores']) * 100

    c1, c2 = st.columns(2)
    with c1: st.line_chart(df.set_index('Cores')['Speedup'])
    with c2: st.bar_chart(df.set_index('Cores')['Efficiency'])

    s_frac = df['Serial'].mean() / df['Time'].iloc[0]
    st.info(f"Serial Fraction (s): {s_frac:.4f} | Max Theoretical Speedup: {1/s_frac:.2f}x")