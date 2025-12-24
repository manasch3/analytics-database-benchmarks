# 📊 Analytics Database Benchmarks  
**Redis · ClickHouse · TimescaleDB · StarRocks**

---

## 📌 What This Research Is About

This project is a **practical, engineering-driven benchmarking study** of modern analytics databases, focused on **how different database architectures behave under real analytics workloads**.

Instead of theoretical comparisons, this research answers a very direct question:

> **“If I am building a SaaS analytics platform today, which database actually performs better, scales better, and is easier to live with?”**

To answer this, I designed and implemented **four versions of the same analytics system**, each backed by a different database engine:

- **v1 – Redis** (baseline, counters-only)
- **v2 – ClickHouse** (columnar analytics engine)
- **v3 – TimescaleDB** (PostgreSQL-based time-series)
- **v4 – StarRocks** (distributed OLAP engine)

Each version uses:
- The **same data model**
- The **same ingestion logic**
- The **same API patterns**
- The **same load-testing configuration**
- Roughly **~50 million events**

The goal is not to “prove one database is best”, but to **understand *why* their performance differs** and **what trade-offs an engineer actually makes** when choosing one.

---

## 🧭 My Approach: v1 → v4 (Why This Order Matters)

This project intentionally progresses from **simple → complex** systems.

### v1 – Redis (Baseline Thinking)
I started with Redis to establish:
- A **performance baseline**
- The absolute minimum overhead possible
- A clear understanding of *what analytics is NOT*

Redis helps answer:
> “How fast can things get if we remove almost all database features?”

---

### v2 – ClickHouse (Analytics-First Design)
ClickHouse represents a **pure analytics database**:
- Columnar storage
- Vectorized execution
- Designed specifically for scans and aggregations

This version tests:
> “What happens when the database is built *only* for analytics?”

---

### v3 – TimescaleDB (Real-World Trade-offs)
TimescaleDB is widely used in production systems.
It brings:
- PostgreSQL compatibility
- ACID guarantees
- Time-series optimizations

This stage evaluates:
> “What performance do we trade for flexibility, SQL familiarity, and safety?”

---

### v4 – StarRocks (Distributed OLAP Reality)
StarRocks is built for **large-scale distributed analytics**.

This final version explores:
> “What happens when a system designed for clusters is run in a constrained, single-node environment?”

---

## 🧪 Test Methodology (Controlled & Reproducible)

> [!IMPORTANT]
> Every database was tested under **identical conditions** to ensure fairness.

**Environment**
- Docker-based local deployment
- Same machine, same resources
- Same dataset size (~50M events)

**Load Test Configuration**
- Threads: **10**
- Duration: **30 seconds**
- Metrics considered:
  - Requests/sec
  - Average latency
  - Tail latency (P95, P99)

---

## 📈 Key Benchmark Results (Essential Values Only)

### ClickHouse (v2)
- **~435 req/sec**
- **~23 ms average latency**

### TimescaleDB (v3)
- **~219 req/sec**
- **~46 ms average latency**

### StarRocks (v4)
- **~26 req/sec**
- **~37 ms average latency**

> These values are sufficient to understand relative behavior without clutter.

---

## 🧠 Analysis Requested by Management

The following sections directly address the requested evaluation criteria:

---

## 1️⃣ Latency

| Database | Latency Characteristics |
|-------|--------------------------|
| Redis | Extremely low (in-memory, simple ops) |
| ClickHouse | **Lowest among analytics systems** |
| TimescaleDB | Higher due to PostgreSQL overhead |
| StarRocks | Moderate, but inconsistent locally |

**Why ClickHouse wins:**  
Columnar reads + vectorized execution minimize CPU and I/O overhead during scans.

---

## 2️⃣ Ease of Use

| Database | Ease of Use |
|-------|-------------|
| Redis | Very easy, but limited |
| ClickHouse | Moderate learning curve |
| TimescaleDB | **Easiest for SQL users** |
| StarRocks | Operationally complex |

**Observation:**  
TimescaleDB feels familiar, but that familiarity comes with performance cost.

---

## 3️⃣ Scale of Ingestion

| Database | Ingestion Scaling |
|-------|------------------|
| Redis | Not suitable for large analytics ingestion |
| ClickHouse | **Excellent bulk ingestion** |
| TimescaleDB | Good, but WAL-bound |
| StarRocks | Designed for massive scale (not shown locally) |

**Why ClickHouse scales best:**  
Append-only, batch inserts, no transactional bookkeeping.

---

## 4️⃣ Maintenance Overhead

| Database | Maintenance Effort |
|-------|-------------------|
| Redis | Low |
| ClickHouse | Low–Moderate |
| TimescaleDB | Medium |
| StarRocks | **High** |

**Real difficulty faced:**  
StarRocks introduces FE/BE separation, metadata handling, and storage management — heavy for small teams.

---

## 5️⃣ Adaptability

| Database | Adaptability |
|-------|-------------|
| Redis | Counters only |
| ClickHouse | Analytics-first |
| TimescaleDB | **Most flexible** |
| StarRocks | OLAP-focused |

**Insight:**  
TimescaleDB adapts well to mixed workloads, but sacrifices raw analytics speed.

---

## 6️⃣ Cost Considerations

| Database | Cost Profile |
|-------|-------------|
| Redis | High RAM cost |
| ClickHouse | **Best cost-to-performance** |
| TimescaleDB | Moderate (CPU + storage + WAL) |
| StarRocks | High infra + ops cost |

---

## 🧠 Why Performance Differs (Core Reasoning)

Performance differences directly map to **internal architecture**:

- **Columnar vs Row-based storage**
- **Vectorized execution vs tuple processing**
- **Append-only ingestion vs transactional writes**
- **Single-node optimization vs distributed coordination**

ClickHouse wins because it:
- Reads only required columns
- Processes data in CPU-friendly batches
- Avoids transactional overhead entirely

TimescaleDB slows down because:
- Every write touches WAL
- Query planner and indexes add latency
- Row-based scans are expensive at scale

StarRocks underperforms here because:
- It is designed for **clusters**, not laptops
- Coordination overhead dominates in local setups

---

## ⚠️ Practical Difficulties Faced

This project surfaced **real engineering challenges**, including:

- Managing **Docker storage explosion** (StarRocks BE storage)
- Handling **schema consistency** across engines
- Debugging ingestion bottlenecks
- Balancing benchmark realism vs system limits
- Avoiding misleading results from misconfigured clusters

These challenges are part of the research outcome, not mistakes.

---

## 📊 Final Comparison Table (Executive View)

| Dimension | ClickHouse | TimescaleDB | StarRocks |
|:--|:--:|:--:|:--:|
| Latency | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Throughput | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| Ease of Use | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Ingestion Scale | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Maintenance | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost Efficiency | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## ✅ Final Recommendation

> [!IMPORTANT]
> **ClickHouse is the most suitable choice for analytics-heavy SaaS platforms.**

**Why:**
- Best latency and throughput
- Scales efficiently to tens of millions of events
- Lower operational burden
- Strong cost-to-performance ratio

TimescaleDB remains a strong choice for **time-series + transactional** systems, while StarRocks should be considered **only when operating real clusters at scale**.

---

## 🧠 Key Takeaways

- Database internals define performance more than hardware
- Columnar analytics engines dominate read-heavy workloads
- Flexibility and familiarity come with measurable cost
- Distributed systems need distributed environments to shine

---

**This repository represents a complete, practical, A–Z evaluation of analytics databases based on real measurements, real constraints, and real engineering trade-offs.**


