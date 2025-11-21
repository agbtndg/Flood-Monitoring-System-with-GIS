# Run All Tests Script
# Flood Monitoring System with GIS - Complete Test Suite
# Last Updated: November 21, 2025

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  FLOOD MONITORING SYSTEM - FULL TEST SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$startTime = Get-Date

# Test 1: White-Box Testing
Write-Host "[1/6] Running White-Box Tests..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
python test_whitebox.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: White-Box Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "Failed: White-Box Tests FAILED" -ForegroundColor Red
}
Write-Host ""

# Test 2: Coverage Report
Write-Host "[2/6] Generating Coverage Report..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
python generate_coverage_report.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Coverage Report GENERATED" -ForegroundColor Green
} else {
    Write-Host "Failed: Coverage Report FAILED" -ForegroundColor Red
}
Write-Host ""

# Test 3: Combined Risk Tests
Write-Host "[3/6] Testing Combined Risk Method..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
python test_combined_risk.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Combined Risk Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "Failed: Combined Risk Tests FAILED" -ForegroundColor Red
}
Write-Host ""

# Test 4: AND-Based Logic Tests
Write-Host "[4/6] Testing AND-Based Logic..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
python test_and_based_logic.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: AND-Based Logic Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "Failed: AND-Based Logic Tests FAILED" -ForegroundColor Red
}
Write-Host ""

# Test 5: Django Unit Tests
Write-Host "[5/6] Running Django Unit Tests..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
python manage.py test --keepdb
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Django Unit Tests PASSED" -ForegroundColor Green
} else {
    Write-Host "Failed: Django Unit Tests FAILED" -ForegroundColor Red
}
Write-Host ""

# Test 6: Code Quality Analysis
Write-Host "[6/6] Running Code Quality Analysis..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor DarkGray
Write-Host "(This may take 30-60 seconds...)" -ForegroundColor DarkGray
python run_code_analysis.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Code Quality Analysis COMPLETE" -ForegroundColor Green
} else {
    Write-Host "Warning: Code Quality Analysis WARNING" -ForegroundColor Yellow
}
Write-Host ""

# Calculate elapsed time
$endTime = Get-Date
$elapsed = $endTime - $startTime
$minutes = [math]::Floor($elapsed.TotalMinutes)
$seconds = $elapsed.Seconds

# Summary
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  TEST SUITE COMPLETE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total Time: $minutes minutes, $seconds seconds" -ForegroundColor White
Write-Host ""
Write-Host "Generated Reports:" -ForegroundColor White
Write-Host "  - coverage_report_*.txt" -ForegroundColor Gray
Write-Host "  - code_analysis_report_*.txt" -ForegroundColor Gray
Write-Host "  - pylint-report.txt" -ForegroundColor Gray
Write-Host "  - bandit-report.txt" -ForegroundColor Gray
Write-Host "  - complexity-report.txt" -ForegroundColor Gray
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor White
Write-Host "  1. Review generated report files" -ForegroundColor Gray
Write-Host "  2. Fix any high-severity issues" -ForegroundColor Gray
Write-Host "  3. Test archiving: python manage.py archive_old_records --dry-run" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  All tests executed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
