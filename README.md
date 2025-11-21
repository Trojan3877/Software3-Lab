# 🧬 Software-3.0 Lab

# Software3-Lab  
### Advanced OOP Simulation Framework + MCP + LLaMA 2 Integration  
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Build](https://img.shields.io/github/actions/workflow/status/Trojan3877/Software3-Lab/ci.yaml?label=CI)
![Lint](https://img.shields.io/github/actions/workflow/status/Trojan3877/Software3-Lab/lint.yaml?label=Linting)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Issues](https://img.shields.io/github/issues/Trojan3877/Software3-Lab)
![Last Commit](https://img.shields.io/github/last-commit/Trojan3877/Software3-Lab)

---

## 📌 Overview
**Software3-Lab** has evolved from a course lab into a **full L5/L6-quality object-oriented simulation framework** with:

- 🚀 Full transportation hierarchy (Motorcycle, MotorVehicle, Airplane, JetPlane)  
- 🧠 LLaMA 2 (or LLaMA 3) LLM integration for explanations, summaries & reasoning  
- 🛰 MCP (Model Context Protocol) integration for controlling simulation objects  
- 🧩 Modular architecture using modern Python package patterns  
- 🛠 Production-ready core modules (BaseModel, ObjectRegistry, Logging)  
- 🧪 Full test suite (pytest) + GitHub Actions CI/CD  
- 🐳 Docker support  
- 🔍 Professional observability (logging, telemetry)  

This project demonstrates **OOP mastery**, **AI integration**, **system design**, and **software engineering rigor** for ML/AI engineering roles.

---

## 🗂 Project Structure

```
Software3-Lab/
│
├── src/
│   ├── core/
│   │   ├── base_model.py
│   │   ├── object_registry.py
│   │   └── __init__.py
│   │
│   ├── oop_labs/
│   │   ├── transport_mode.py
│   │   ├── motor_vehicle.py
│   │   ├── motorcycle.py
│   │   ├── airplane.py
│   │   ├── jet_plane.py
│   │   ├── __init__.py
│   │   └── examples/
│   │       ├── demo_vehicle_sim.py
│   │       ├── demo_registry.py
│   │       └── __init__.py
│   │
│   └── __init__.py
│
├── tests/
├── Dockerfile
├── requirements.txt
├── pyproject.toml
├── README.md
└── .github/workflows/
```

---

## 🧠 LLaMA 2 / LLaMA 3 Integration  
This project supports **local** or **API-based** LLaMA models.

Use the LLaMA client to generate explanations for any object:

### **Example (explain a JetPlane using LLaMA):**
```python
from src.ai.llama_client import LlamaClient
from src.oop_labs.jet_plane import JetPlane

llm = LlamaClient(model="llama2-13b")

jet = JetPlane(
    name="F-22 Raptor",
    max_speed=1500,
    wingspan=44,
    max_altitude=65000,
    num_passengers=1,
    is_military=True,
)

explanation = llm.explain_object(jet)
print(explanation)
```

### **What the LLM can do:**
- Provide OOP explanations  
- Describe object behavior  
- Summarize simulation state  
- Generate natural-language reasoning  
- Assist with debugging  

---

## 🛰 MCP Integration (Model Context Protocol)

You can control and inspect objects in the simulation using the MCP server.

### **Example MCP Calls**
```
mcp call transport.takeoff <jet_id>
mcp call motorcycle.add_fuel <bike_id> gallons=3
mcp get-object <id>
mcp list-objects
```

The server exposes each object in the `ObjectRegistry` and allows:

- Real-time inspection  
- Method invocation  
- State updates  
- Telemetry retrieval  

### **Start the MCP Server**
```
python -m src.mcp.server
```

---

## 🚀 Running the Simulation Demo

### **Vehicle Simulation**
```
python src/oop_labs/examples/demo_vehicle_sim.py
```

### **Registry Inspector**
```
python src/oop_labs/examples/demo_registry.py
```

---

## 🧪 Testing

Run full test suite:

```
pytest -q
```

---

## 🐳 Docker Support

Build:
```
docker build -t software3-lab .
```

Run:
```
docker run -it software3-lab
```

---

## 📌 Key Features (L5/L6 Level)

| Feature | Description |
|--------|-------------|
| **Advanced OOP Architecture** | Deep inheritance hierarchy with vehicles & aircraft |
| **Telemetry Logging** | Loguru-based structured logs |
| **Registry System** | Global object registry with search/index capabilities |
| **LLM Integration** | LLaMA 2/3 for reasoning & explanation |
| **MCP Server** | API-like control mechanism |
| **Professional Structure** | Full src layout, tests, CI/CD |
| **Simulated Physics** | Speed, altitude, fuel systems, EV systems |
| **Airplane & Jet Simulation** | Takeoff, landing, climb, descent, afterburner, Mach speed |

---

## 📄 License  
MIT License — free for personal and professional use.

---

## ⭐ Developer  
**Corey Leath**  
AI/ML Engineer & Software Developer  
GitHub: [@Trojan3877](https://github.com/Trojan3877)

