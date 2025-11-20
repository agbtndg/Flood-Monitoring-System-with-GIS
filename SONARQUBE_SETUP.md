# SonarQube Setup and Analysis Guide
# Flood Monitoring System with GIS - Silay City DRRMO

## What is SonarQube?

SonarQube is a leading platform for continuous inspection of code quality. It performs automatic reviews with static analysis to detect:
- Bugs
- Code smells
- Security vulnerabilities
- Code coverage
- Code duplication
- Complexity metrics
- Technical debt

**Perfect for white-box testing** because it analyzes internal code structure, complexity, and potential issues.

---

## Setup Options

### Option 1: SonarCloud (Recommended for Quick Demo)
**Pros:** Free, no installation, web-based, instant results  
**Cons:** Requires GitHub repository, internet connection

### Option 2: Local SonarQube Server
**Pros:** Complete control, runs offline, enterprise features  
**Cons:** Requires Java, Docker, or dedicated server

### Option 3: SonarLint (IDE Plugin)
**Pros:** Real-time analysis in VS Code  
**Cons:** No centralized reporting

---

## Quick Setup: Local Code Analysis (No Server Required)

For your professor demonstration, we'll use **static analysis tools** that provide SonarQube-style reports without needing the full server.

### Step 1: Run Pylint (Code Quality Analysis)

```powershell
# Analyze all Python files
pylint monitoring users maps --output-format=text > pylint-report.txt

# Or analyze specific modules
pylint monitoring/views.py monitoring/models.py users/models.py
```

**What Pylint checks:**
- Code style (PEP 8 compliance)
- Programming errors
- Code smells
- Unused variables/imports
- Complexity metrics

### Step 2: Run Bandit (Security Analysis)

```powershell
# Security scan
bandit -r monitoring users maps -f json -o bandit-report.json

# Or text format for easier reading
bandit -r monitoring users maps -f txt -o bandit-report.txt
```

**What Bandit checks:**
- SQL injection vulnerabilities
- Hardcoded passwords
- Use of insecure functions
- Shell injection risks
- Cryptography issues

### Step 3: Run Coverage Analysis with Pytest

```powershell
# Install pytest configuration
pytest --cov=monitoring --cov=users --cov-report=html --cov-report=xml

# Or use our existing test
pytest test_whitebox.py --cov=monitoring --cov=users --cov-report=html
```

### Step 4: Generate Complexity Report

```powershell
# Using radon (install if needed)
pip install radon
radon cc monitoring users -a -s

# Cyclomatic complexity
radon cc monitoring/views.py -s
```

---

## Full SonarQube Server Setup (Optional)

If you want the complete SonarQube experience:

### Requirements
- Java 17 or higher
- 2GB RAM minimum
- Windows/Linux/Mac

### Installation Steps

#### Method 1: Docker (Easiest)

```powershell
# Pull SonarQube image
docker pull sonarqube:latest

# Run SonarQube server
docker run -d --name sonarqube -p 9000:9000 sonarqube:latest

# Access: http://localhost:9000
# Default credentials: admin/admin
```

#### Method 2: Direct Download

1. **Download SonarQube Community Edition**
   - Go to: https://www.sonarqube.org/downloads/
   - Download: Community Edition (free)
   - Extract to: C:\sonarqube

2. **Start SonarQube Server**
   ```powershell
   cd C:\sonarqube\bin\windows-x86-64
   StartSonar.bat
   ```

3. **Access Web Interface**
   - URL: http://localhost:9000
   - Login: admin / admin
   - Change password on first login

4. **Download SonarScanner**
   - Go to: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/
   - Download: SonarScanner CLI
   - Extract to: C:\sonar-scanner
   - Add to PATH: C:\sonar-scanner\bin

5. **Run Analysis**
   ```powershell
   # From project directory
   sonar-scanner.bat
   ```

---

## SonarCloud Setup (Free for Public Repos)

### Steps

1. **Sign up for SonarCloud**
   - Go to: https://sonarcloud.io
   - Sign in with GitHub
   - Import your repository

2. **Get Token**
   - My Account → Security → Generate Token
   - Copy token

3. **Run Analysis**
   ```powershell
   # Install sonar-scanner
   npm install -g sonarqube-scanner
   
   # Run scan
   sonar-scanner `
     -Dsonar.organization=your-org `
     -Dsonar.projectKey=flood-monitoring-system `
     -Dsonar.sources=. `
     -Dsonar.host.url=https://sonarcloud.io `
     -Dsonar.login=your-token
   ```

---

## Alternative: Run Analysis Without SonarQube Server

I've created a script that generates SonarQube-style reports using available tools:

```powershell
python run_code_analysis.py
```

This will generate:
- Code quality report (Pylint)
- Security analysis (Bandit)
- Complexity metrics (Radon)
- Coverage report
- Combined dashboard report

---

## Interpreting Results

### Quality Gates (SonarQube Standards)

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Code Coverage | >80% | 70-80% | <70% |
| Bugs | 0 | 1-5 | >5 |
| Vulnerabilities | 0 | 0 | >0 |
| Code Smells | <10/kloc | 10-20/kloc | >20/kloc |
| Duplications | <3% | 3-5% | >5% |
| Complexity | <10 | 10-15 | >15 |

### Pylint Scores
- **10.0** - Perfect (rare)
- **8.0+** - Excellent
- **7.0-8.0** - Good
- **6.0-7.0** - Acceptable
- **<6.0** - Needs improvement

### Bandit Severity
- **High** - Critical security issues (fix immediately)
- **Medium** - Potential security risks (review)
- **Low** - Best practice recommendations

---

## For Your Professor Demonstration

### Quick Demo Path (No Installation)

1. **Run Pylint Analysis**
   ```powershell
   pylint monitoring users --output-format=text | Tee-Object -FilePath pylint-report.txt
   ```

2. **Run Security Scan**
   ```powershell
   bandit -r monitoring users -f txt | Tee-Object -FilePath bandit-report.txt
   ```

3. **Show Reports**
   - Open `pylint-report.txt` - Code quality
   - Open `bandit-report.txt` - Security
   - Reference existing coverage report - 76.7%

4. **Highlight Metrics**
   - Code quality score (Pylint)
   - Security vulnerabilities found (Bandit)
   - Test coverage (Already have 76.7%)
   - Complexity analysis

### Full Demo Path (With Analysis Script)

```powershell
# Run comprehensive analysis
python run_code_analysis.py

# Opens interactive report with:
# - Code quality metrics
# - Security analysis
# - Complexity breakdown
# - Coverage statistics
# - Overall quality grade
```

---

## Benefits for White-Box Testing

SonarQube enhances white-box testing by:

1. **Static Analysis** - Analyzes code without execution
2. **Complexity Metrics** - Cyclomatic complexity, cognitive complexity
3. **Code Coverage** - Identifies untested code paths
4. **Duplicate Detection** - Finds copy-pasted code
5. **Security Scanning** - Identifies vulnerabilities
6. **Technical Debt** - Estimates maintenance cost
7. **Trend Analysis** - Tracks quality over time

---

## Next Steps

Choose your preferred method:

**A. Quick Analysis (5 minutes)**
```powershell
# Run basic analysis
pylint monitoring users
bandit -r monitoring users
```

**B. Comprehensive Report (10 minutes)**
```powershell
# Run analysis script
python run_code_analysis.py
```

**C. Full SonarQube (30+ minutes)**
- Install Docker
- Run SonarQube container
- Execute scanner
- View web dashboard

---

## Troubleshooting

### Pylint Issues
```powershell
# If Django imports fail
pylint --load-plugins=pylint_django monitoring
pip install pylint-django
```

### Bandit Issues
```powershell
# Ignore specific warnings
bandit -r monitoring --skip B101,B601
```

### Coverage Issues
```powershell
# Set Django settings
$env:DJANGO_SETTINGS_MODULE = "silay_drrmo.settings"
pytest --cov=monitoring --cov=users
```

---

## Files Created

- `sonar-project.properties` - SonarQube configuration
- `SONARQUBE_SETUP.md` - This guide
- `run_code_analysis.py` - Automated analysis script

---

**Ready to proceed?** Choose your analysis method and I'll help you run it!
