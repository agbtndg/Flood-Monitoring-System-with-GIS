# Testing Guide - Flood Monitoring System with GIS

## Testing Framework and Tools

This project uses **Django's built-in testing framework** based on Python's `unittest` library, which provides a robust testing infrastructure specifically designed for web applications. Django's `TestCase` class extends Python's `unittest.TestCase` and includes automatic test database creation and destruction (creating a temporary database before each test and destroying it afterward), transaction management (wrapping each test in a transaction that's rolled back after completion for test isolation), a test client (a dummy web browser for simulating GET/POST requests without running a server), easy creation of test data using Django models, and special assertions for testing Django-specific functionality such as templates, redirects, and form validation, making it ideal for comprehensively testing our flood monitoring system.

### How Tests Work in Our System

```python
# Example of a typical test in our system
class MapViewTest(TestCase):
    def setUp(self):
        # Runs before each test - creates test data
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_map_view_requires_login(self):
        # Test that unauthenticated users are redirected
        response = self.client.get('/maps/')
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_map_view_loads_for_authenticated_user(self):
        # Login and test that page loads
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/maps/')
        self.assertEqual(response.status_code, 200)  # Success
        self.assertTemplateUsed(response, 'maps/map.html')
```

### Test Execution Process

1. **Test Discovery** - Django automatically finds all files named `tests.py` or matching `test*.py`
2. **Database Setup** - Creates a temporary PostgreSQL database with PostGIS extension
3. **Migration Application** - Applies all migrations to create the test database schema
4. **Test Execution** - Runs each test method in isolation:
   - Calls `setUp()` to prepare test data
   - Executes the test method
   - Calls `tearDown()` to clean up (automatic)
   - Rolls back any database changes
5. **Database Teardown** - Destroys the temporary test database
6. **Results Reporting** - Shows pass/fail status, error details, and execution time

### Running Tests

```powershell
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test maps
python manage.py test monitoring
python manage.py test users

# Run a specific test class
python manage.py test maps.tests.MapViewTest

# Run a specific test method
python manage.py test maps.tests.MapViewTest.test_map_view_requires_login

# Run with verbose output
python manage.py test --verbosity=2
```

### Test Types in Our System

1. **Model Tests** - Verify database models, fields, methods, and constraints
2. **View Tests** - Test HTTP endpoints, authentication, permissions, and responses
3. **Form Tests** - Validate form validation, error handling, and data cleaning
4. **Integration Tests** - Test complete workflows (registration → approval → login)
5. **Admin Tests** - Verify Django admin interface configuration
6. **Template Tests** - Ensure templates render correctly with proper context

---

## Test Suite Summary

The Flood Monitoring System with GIS has achieved **100% test pass rate** with **273 comprehensive tests** covering all major functionality across three Django apps: Maps (112 tests for GIS functionality, activity tracking, and flood susceptibility mapping), Monitoring (80 tests for weather data, rainfall/tide monitoring, and risk calculations with configurable BenchmarkSettings), and Users (81 tests for authentication, user management, profiles, and activity logging), ensuring complete feature coverage including user authentication, GIS mapping, flood risk algorithms, weather monitoring, data export, activity tracking, admin workflows, and form validation.

### Breakdown by Django App

#### 1. Maps App - 112 Tests ✅

The maps app handles GIS functionality, activity tracking, and flood susceptibility mapping.

**Test Classes:**
- `MapViewTest` (4 tests) - GIS map display and GeoJSON serialization
- `BarangayModelTest` (3 tests) - Barangay model and geometry handling
- `FloodSusceptibilityModelTest` (7 tests) - Flood hazard classification (LF/MF/HF/VHF)
- `AssessmentRecordModelTest` (1 test) - Flood risk assessments
- `ReportRecordModelTest` (1 test) - Report generation records
- `CertificateRecordModelTest` (2 tests) - Certificate issuance tracking
- `FloodRecordActivityModelTest` (4 tests) - Flood event documentation
- `SaveAssessmentViewTest` (5 tests) - Risk assessment creation
- `ReportViewTest` (10 tests) - Report generation with recommendations
- `CertificateViewTest` (4 tests) - Certificate generation
- `CertificateFormViewTest` (7 tests) - Certificate form handling
- `MyActivityViewTest` (8 tests) - User's personal activity dashboard
- `AllActivitiesViewTest` (8 tests) - Staff activity monitoring
- `ExportActivitiesViewTest` (11 tests) - CSV/PDF export with filtering
- `ErrorViewTest` (5 tests) - Custom error page handling
- `PrivacyPolicyViewTest` (2 tests) - Privacy policy page
- `TermsOfServiceViewTest` (2 tests) - Terms of service page
- **Admin Tests** (28 tests) - Django admin interface for all models

**Key Features Tested:**
- ✅ PostGIS geometry operations (Point, MultiPolygon)
- ✅ GeoJSON serialization for OpenLayers integration
- ✅ Flood risk classification (4 levels: Low/Moderate/High/Very High)
- ✅ Activity tracking with pagination and filtering
- ✅ CSV/PDF export with date ranges, search, and sorting
- ✅ Archiving system for records
- ✅ Permission-based access control (login required, staff-only views)
- ✅ Public pages (privacy policy, terms of service)

**Issues Fixed:**
- Changed `.count()` to `len()` for paginated Page objects (2 tests)
- Page objects from Django Paginator don't have a `.count()` method like QuerySets

---

#### 2. Monitoring App - 80 Tests ✅

The monitoring app manages weather data, rainfall/tide monitoring, and flood risk calculations.

**Test Classes:**
- `RainfallDataModelTest` (4 tests) - Rainfall measurement storage
- `TideDataModelTest` (4 tests) - Tide level measurement storage
- `WeatherForecastModelTest` (4 tests) - Weather forecast data
- `FloodRecordModelTest` (6 tests) - Historical flood event tracking
- `BenchmarkSettingsModelTest` (5 tests) - Configurable risk thresholds
- `BenchmarkSettingsViewTest` (10 tests) - Admin threshold configuration
- `DashboardViewTest` (11 tests) - Main monitoring dashboard
- `FloodRiskLevelFunctionTest` (11 tests) - Risk calculation algorithms
- `GenerateFloodInsightsTest` (7 tests) - AI-powered flood predictions
- `UpdateRainfallDataViewTest` (10 tests) - Rainfall data management
- `UpdateTideDataViewTest` (8 tests) - Tide data management

**Key Features Tested:**
- ✅ Real-time weather data processing
- ✅ Configurable benchmark thresholds (BenchmarkSettings model)
- ✅ 3-level risk system: Low (yellow), Moderate (orange), High (red)
- ✅ AND-based threshold logic for combined risk assessment
- ✅ 4 calculation methods: Maximum, Rainfall Priority, Tide Priority, Equal Weight
- ✅ Historical data tracking with timestamps
- ✅ Flood insights generation with severity levels
- ✅ AJAX endpoints for real-time updates
- ✅ Staff-only access controls

**Issues Fixed:**
- Updated from 4-level (Low/Moderate/High/Critical) to 3-level risk system (12 tests)
- Changed color scheme: green/yellow/orange/red → yellow/orange/red
- Fixed `get_combined_risk_level()` to accept numeric values instead of strings (3 tests)
- Updated insights test to use values exceeding high threshold (50mm)

**New Features Added:**
- 15 new tests for BenchmarkSettings (model + view tests)
- Complete coverage of configurable threshold system
- Validation for threshold ordering (moderate < high)
- Metadata tracking (updated_by, updated_at)

---

#### 3. Users App - 81 Tests ✅

The users app handles authentication, user management, profiles, and activity logging.

**Test Classes:**
- `CustomUserModelTest` (9 tests) - Custom user model with staff_id
- `UserLogModelTest` (3 tests) - Activity logging timestamps
- `CustomUserCreationFormTest` (10 tests) - Registration form validation
- `CustomUserChangeFormTest` (6 tests) - Profile update form
- `UserLoginViewTest` (6 tests) - Authentication system
- `UserLogoutViewTest` (1 test) - Session termination
- `UserRegisterViewTest` (6 tests) - New user registration
- `AdminRegisterViewTest` (7 tests) - Admin account creation
- `UserApprovalViewTest` (5 tests) - Admin user approval
- `UserListViewTest` (8 tests) - User management interface
- `ViewProfileViewTest` (6 tests) - Profile viewing and editing
- `PasswordStrengthValidatorTest` (5 tests) - Password security rules
- `AgeValidatorTest` (5 tests) - Age restriction (18-80 years)
- `ContactNumberValidatorTest` (4 tests) - Philippine phone number format

**Key Features Tested:**
- ✅ Custom user model with extended fields (staff_id, position, contact_number, bio)
- ✅ Auto-generated staff ID (format: YEAR + 4-digit sequential number)
- ✅ Two-step registration: User registers → Admin approves
- ✅ Secure admin registration with registration key
- ✅ Role-based permissions (staff, admin, superuser)
- ✅ Profile management with avatar uploads
- ✅ Password strength requirements (uppercase, lowercase, digits, special chars)
- ✅ Age validation (18-80 years old)
- ✅ Philippine phone number validation (11 digits)
- ✅ Custom position field when selecting "Others"
- ✅ User activity logging (login, logout, profile updates)

**Issues Fixed:**
- Added `custom_position` field to 4 tests when `position='others'` (form validation requirement)
- Form validation requires custom_position when position is 'others'
- Fixed contact number uniqueness in sequential test (changed from duplicate to unique)

---

## Key Testing Achievements

### 1. Complete Feature Coverage
Every major feature has corresponding tests:
- ✅ User authentication and authorization
- ✅ GIS mapping and spatial data
- ✅ Flood risk assessment algorithms
- ✅ Weather monitoring and forecasting
- ✅ Data export (CSV/PDF)
- ✅ Activity tracking and archiving
- ✅ Admin approval workflows
- ✅ Form validation and security

### 2. Test Quality Metrics
- **Comprehensive assertions** - Each test verifies multiple aspects (status code, template, context, database state)
- **Proper isolation** - Tests don't depend on each other
- **Realistic data** - Test data mirrors production scenarios
- **Edge cases covered** - Tests include boundary conditions, invalid inputs, and error scenarios

### 3. Regression Prevention
Tests ensure that:
- New features don't break existing functionality
- Code refactoring maintains behavior
- Database schema changes are compatible
- Form validation rules are enforced
- Security measures remain in place

### 4. Documentation Value
Tests serve as:
- **Living documentation** - Shows how features should behave
- **API examples** - Demonstrates correct usage of views and models
- **Integration guides** - Illustrates how components work together

---

## Testing Best Practices Followed

1. **Descriptive test names** - Test methods clearly state what they verify
2. **Arrange-Act-Assert pattern** - Setup data, perform action, verify result
3. **One concept per test** - Each test focuses on a single behavior
4. **setUp/tearDown usage** - Proper test data initialization and cleanup
5. **DRY principle** - Common test utilities extracted to helper methods
6. **Meaningful assertions** - Clear error messages when tests fail

---

## Maintenance and Future Testing

### Adding New Tests
When adding features, ensure to add tests for:
1. Model creation and validation
2. View permissions and access control
3. Form validation and error handling
4. Template rendering and context
5. Integration with existing features

### Running Tests in CI/CD
Tests can be integrated into continuous integration pipelines:
```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    python manage.py test --verbosity=2
    python manage.py test --keepdb --parallel
```

### Test Database Performance
For faster test execution:
- Use `--keepdb` flag to reuse test database
- Use `--parallel` to run tests in parallel
- Consider using SQLite for faster test database creation (in CI only)

---

## Conclusion

The Flood Monitoring System with GIS has achieved **100% test pass rate** across 273 tests covering all major functionality. The test suite provides:

✅ **Confidence** - Changes can be made knowing tests will catch regressions  
✅ **Documentation** - Tests demonstrate how the system works  
✅ **Quality** - High test coverage ensures reliability  
✅ **Maintainability** - Tests make refactoring safer and easier  

The comprehensive test coverage ensures that the flood monitoring system is robust, reliable, and ready for production deployment. All critical features including GIS mapping, risk assessment, weather monitoring, user management, and data export have been thoroughly tested and validated.
