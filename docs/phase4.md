# Architecture

tests/
   ↓
pytest fixture
   ↓
DriverManager
   ↓
Appium Options / Capabilities
   ↓
Appium Server
   ↓
Android Emulator

# New Flow
pytest
  │
  ▼
driver fixture
  │
  ▼
DriverManager
  │
  ▼
UiAutomator2Options
  │
  ▼
Appium :4723
  │
  ▼
UiAutomator2
  │
  ▼
Android Emulator