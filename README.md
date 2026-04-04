# DevSecOps Pipeline Research — ShopSecure

## Research Overview
This project investigates the security-overhead trade-off of integrating 
automated security tools into CI/CD pipelines for small development teams.

## Experimental Design
Four pipeline configurations were tested across 4 runs each:

| Experiment | Configuration | Avg Time | Overhead |
|---|---|---|---|
| 1 | Baseline (no security) | 18.5s | — |
| 2 | + Dependency Scan (Safety) | 29.3s | +10.8s |
| 3 | + Dependency + SAST (Bandit) | 27.3s | +8.8s |
| 4 | + Container Scan (Trivy) | 51.8s | +33.3s |

## Vulnerability Findings

| Tool | Vulnerabilities Detected |
|---|---|
| Safety (dependency scan) | 44 across 9 packages |
| Bandit (SAST) | 11 issues (3 High, 3 Medium, 5 Low) |
| Trivy (container scan) | 41 total (5 Critical, 36 High) |

## Bandit SAST Findings (by category)
- **MD5 weak hashing** — `app/auth.py` (CWE-327)
- **Command injection** via shell=True — `app/auth.py` (CWE-78)
- **SQL injection** via string formatting — `app/models.py` (CWE-89)
- **Insecure deserialization** via pickle — `app/payments.py` (CWE-502)
- **Flask debug mode** exposed — `app/main.py` (CWE-94)

## Target Application
ShopSecure is a realistic e-commerce REST API built with Flask, consisting 
of four modules: authentication, products, orders, and payments. It uses 
SQLite for persistence and JWT for authentication. Intentional vulnerabilities 
are embedded throughout to serve as realistic scan targets.

## Security Tools
- **Safety** — dependency vulnerability scanning
- **Bandit** — static application security testing (SAST)
- **Trivy** — container image scanning

## Running Locally
```bash
pip install -r requirements.txt
python -m app.main
```

## Research Question
What is the security-overhead trade-off of incrementally adding automated 
security tools to a CI/CD pipeline for small development teams?