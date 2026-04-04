# Research Observations and Analysis

## Experiment Results Summary
Four pipeline configurations were tested with 4 runs each to ensure 
consistency and remove the effect of GitHub runner variability.

## Key Observations

### 1. Trivy container scanning dominates overhead
The biggest overhead jump occurs between Experiment 3 and Experiment 4 — 
adding Trivy container scanning adds approximately 24 seconds on average. 
This is because Trivy pulls and scans the entire Docker image layer by layer, 
inspecting both OS-level packages and Python dependencies. For small teams 
with limited CI/CD minutes, this is the most significant cost.

### 2. Bandit SAST adds minimal overhead
Going from Experiment 2 to Experiment 3 actually showed no additional overhead 
— Experiment 3 averaged slightly faster than Experiment 2 due to GitHub runner 
variability. This suggests that SAST scanning with Bandit is essentially free 
in terms of pipeline time, making it a high-value low-cost addition for small teams.

### 3. Runner variability affects results
Across 4 runs, individual times varied by up to 8 seconds for the same 
configuration (e.g. Experiment 4 ranged from 47s to 55s). This confirms 
the importance of multiple runs and averaging rather than relying on a 
single measurement.

### 4. Dependency scanning catches the most vulnerabilities
Safety detected 44 vulnerabilities across 9 packages — far more than 
Bandit's 11 code-level issues. However, many of these are in transitive 
dependencies (packages installed by other packages) rather than direct 
dependencies, which limits their immediate actionability for small teams.

### 5. SAST findings directly map to intentional vulnerabilities
Bandit correctly identified all major intentionally embedded vulnerabilities:
- MD5 weak hashing (CWE-327)
- Command injection via shell=True (CWE-78)
- SQL injection via string formatting (CWE-89)
- Insecure deserialization via pickle (CWE-502)
- Flask debug mode exposed (CWE-94)

This validates the experimental design — the tools are detecting real 
security issues, not false positives.

### 6. Trivy provides layered coverage
Trivy found 41 vulnerabilities split across OS-level packages (19) and 
Python packages (22). Notably it detected issues in the base Docker image 
itself (debian:13.1) including 3 Critical OpenSSL vulnerabilities — 
something neither Safety nor Bandit can detect. This demonstrates the 
unique value of container scanning as a third layer.

### 7. SAST limitations observed
Bandit did not flag hardcoded secrets (SECRET_KEY, PAYMENT_API_KEY) under 
the severity thresholds used (-ll -ii flags). This is a known limitation 
of threshold-based SAST configuration and suggests that tool configuration 
choices significantly affect detection coverage — an important finding for 
the trade-off model.

## Implications for Small Teams
Based on the experimental data, the recommended minimum viable DevSecOps 
configuration for a small team is Experiments 2+3 combined (Safety + Bandit) 
at an average overhead of 27 seconds. This configuration catches dependency 
vulnerabilities and code-level security issues at minimal pipeline cost. 
Container scanning (Trivy) should be added when Docker is used in production, 
accepting the additional 24 second overhead in exchange for OS-level and 
image-level vulnerability coverage.