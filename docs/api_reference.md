# 📚 Software-3-Lab — API Reference

> Base URL (local dev)  
> `http://localhost:8080`

For deployed environments, replace host with your K8s LoadBalancer / Ingress URL.

---

## 1. Health & Metadata

| Method | Path | Description | Response |
|--------|------|-------------|----------|
| GET | `/` | Basic liveness check | `{"status":"ok"}` |
| GET | `/metrics` | Prometheus metrics scrape endpoint (latency, cost) | `text/plain; version=0.0.4` |
| GET | `/registry` | List fine-tune model entries | JSON array |

---

## 2. Feedback Collection

| Method | Path | Body | Response |
|--------|------|------|----------|
| POST | `/feedback` | `{ "prompt": "...", "response": "...", "rating": 4, "comments": "" }` | `{"msg":"saved","ts":"2025-06-30T14:12:00Z"}` |

---

## 3. Fine-Tune Trigger

| Method | Path | Body | Response |
|--------|------|------|----------|
| POST | `/fine_tune` | `{ "base_model": "gpt-3.5-turbo" }` | `{ "job_id": "...", "status": "queued" }` |

---

## 4. Evaluation

| Method | Path | Query | Response |
|--------|------|-------|----------|
| POST | `/evaluate` | `model=ft:gpt-3.5-turbo:2025-06-30` | `{ "rougeL": 0.46, "bleu4": 0.34, "pass@3": 0.78 }` |

### Batch Evaluation

```bash
curl -X POST http://localhost:8080/evaluate \
     -H "Content-Type: application/json" \
     -d '{"model":"latest","benchmark":"default"}'
