# 🚇 Delhi Metro Route & Schedule Simulator

A **fully terminal-based Python simulator** that models the **Delhi Metro system** using real-world data.  
The program allows users to **check upcoming metro timings** at any station and **plan optimized journeys** between stations with accurate handling of **interchanges, schedules, travel time, fare, and carbon savings**.

This project is designed as a **system simulation + algorithmic routing problem**, not a UI application.

---

## 📌 Table of Contents

1. Project Motivation  
2. Scope & Objectives  
3. Supported Metro Lines  
4. Data Sources & File Structure  
5. Design Philosophy  
6. Core Assumptions  
7. Constraints & Simplifications  
8. System Architecture Overview  
9. Detailed Module Breakdown  
10. Metro Timings Algorithm  
11. Journey Planner Algorithms  
12. Optimization Strategies  
13. Fare & Carbon Calculation  
14. Time Handling & Edge Cases  
15. Terminal UI Design  
16. Error Handling  
17. Limitations  
18. Future Improvements  
19. How to Run  
20. Folder Structure

---

## 1️⃣ Project Motivation

Delhi Metro is a **time-dependent, graph-like transport network**.  
The goal of this project was to simulate **realistic metro behavior** using:

- Real station data
- Real schedule frequencies
- Accurate travel-time propagation
- Logical interchange handling

Instead of hardcoding outputs, the system **infers arrivals dynamically** based on terminal schedules and station offsets.

This project demonstrates:
- File-based data modeling
- Time arithmetic
- Graph traversal with constraints
- Multi-criteria optimization
- Real-world simulation logic

---

## 2️⃣ Objectives & Scope

The program is designed to:

✔ Compute **next and subsequent metro arrivals** at any station  
✔ Plan a **complete journey** between two stations  
✔ Handle **multi-line interchanges**  
✔ Optimize routes by:
- Minimum total time
- Minimum interchanges  
✔ Provide:
- Step-by-step journey breakdown
- Fare estimation
- Carbon savings estimation

---

## 3️⃣ Supported Metro Lines

| Line | Coverage |
|----|----|
| **Blue Line** | Dwarka Sector 21 ↔ Noida Electronic City |
| **Blue Branch** | Yamuna Bank ↔ Vaishali |
| **Magenta Line** | Janakpuri West ↔ Botanical Garden |
| **Yellow Line** | Samaypur Badli ↔ Millennium City Centre |

---

## 4️⃣ Data Sources & Files

All data is **manually collected from the official DMRC website** and stored in plain text files.

### 📄 `Metro Data.txt`
Each row represents **one segment** between two stations.

```
Line, Station, NextStation, TravelTime(min), Interchange?, [Connecting Line]
```

Example:
```
Blue, Janakpuri West, Janakpuri East, 3, Yes, Magenta
```

Meaning:
- Station belongs to Blue Line
- Travel time to next station is 3 minutes
- Interchange exists with Magenta Line

---

### 📄 `timings.txt`
Stores **origin station departure times** (minutes past the hour).

```
08:00, 04, 08, 12, 16, 20, 24, ...
```

This encodes:
- Peak hours → every 4 minutes
- Off-peak → every 8 minutes

---

## 5️⃣ Design Philosophy

### ❌ What was intentionally NOT used
- No databases
- No pandas / numpy
- No graph libraries
- No datetime arithmetic libraries (except system time)

### ✅ What WAS used
- Plain file I/O
- Lists, dictionaries
- Manual time arithmetic
- Deterministic simulation

The goal was **algorithmic clarity**, not abstraction hiding.

---

## 6️⃣ Core Assumptions

1. **Constant Travel Time**
   - Each station-to-station hop = **3 minutes**

2. **Interchange Delay**
   - Fixed **5 minutes** added for every line change

3. **Train Origins**
   - Timetable applies only at **terminal stations**
   - Arrival times at other stations are inferred

4. **Fare Model**
   - ₹6 per station traveled

5. **Carbon Savings**
   - 150 grams CO₂ saved per station

---

## 7️⃣ Constraints & Simplifications

| Constraint | Reason |
|----|----|
| Fixed travel time | Simplifies routing logic |
| No train overtaking | Metro behavior assumption |
| No express services | All trains stop at every station |
| No service before 06:00 or after 23:00 | DMRC schedule |
| Static timetable | No delays modeled |

---

## 8️⃣ System Architecture Overview

```
User Input
   ↓
Main Menu
   ├── Timings Module
   │      ├── Station Selection
   │      ├── Time Selection
   │      └── Arrival Calculation
   │
   └── Journey Planner
          ├── Start Station
          ├── End Station
          ├── Start Time
          ├── Optimization Strategy
          └── Route Simulation
```

---

## 9️⃣ Detailed Module Breakdown

### 9.1 Data Loading
- Metro data parsed into line-specific lists
- Timings stored as:
```python
{ hour: [list_of_departure_minutes] }
```

### 9.2 Interchange Dictionary
Maps:
```
(Line A, Line B) → [Interchange Stations]
```

Bidirectional by design.

---

## 🔟 Metro Timings Algorithm

### Key Idea
Metro schedules exist **only at terminal stations**.

To find arrival at any station:

```
arrival_time = terminal_departure_time + station_offset
```

### Offset Calculation
```
offset = (station_index - 1) × 3 minutes
```

### Reverse Direction
```
offset = (total_stations - station_index) × 3
```

---

## 1️⃣1️⃣ Journey Planner Logic

The journey planner is the **core algorithmic component**.

### Steps:
1. Identify start & destination lines
2. Generate possible line sequences
3. Identify valid interchange stations
4. Simulate journey for each possibility
5. Select optimal route based on strategy

---

## 1️⃣2️⃣ Optimization Strategies

### Strategy 1: Minimum Time
- Tries **all feasible line paths**
- Simulates every interchange combination
- Chooses earliest arrival

### Strategy 2: Minimum Interchanges
- Uses **predefined optimal line paths**
- Fewer simulations
- Faster but slightly less flexible

---

## 1️⃣3️⃣ Fare & Carbon Calculation

### Fare
```
fare = total_stations × 6
```

### Carbon Savings
```
CO₂ saved = total_stations × 150 grams
```

---

## 1️⃣4️⃣ Time Handling & Edge Cases

Handled scenarios:
- Arrival after midnight → wrapped correctly
- Last train of the day
- No service available
- Station equals destination
- Direction-based terminal logic

---

## 1️⃣5️⃣ Terminal UI Design

Uses **ANSI escape codes** for:
- Color-coded steps
- Icons
- Clear hierarchy

No external UI libraries used.

---

## 1️⃣6️⃣ Error Handling

- Invalid menu input
- Invalid station selection
- Invalid time input
- No-route-available scenarios

System never crashes; it **fails gracefully**.

---

## 1️⃣7️⃣ Limitations

- Fixed travel times
- No live delays
- No real-time crowding
- No express services
- Static metro map

---

## 1️⃣8️⃣ Future Improvements

- Graph-based routing (Dijkstra)
- Real fare slabs
- More metro lines
- GUI or Web interface
- Live API integration

---

## 1️⃣9️⃣ How to Run

```bash
python metro_simulator.py
```

Ensure files are present:
- `Metro Data.txt`
- `timings.txt`

---

## 2️⃣0️⃣ Folder Structure

```
Delhi-Metro-Simulator/
│
├── metro_simulator.py
├── Metro Data.txt
├── timings.txt
├── README.md
```

---

## 🏁 Final Note

This project is intentionally **low-level and explicit** to demonstrate:

✔ Algorithmic thinking  
✔ Real-world system modeling  
✔ Clean logic over abstraction  

---

🚇 *Built to simulate reality, not shortcut it.*
