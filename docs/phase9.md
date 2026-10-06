Git Push / Pull Request
          ↓
   GitHub Actions
          ↓
   Ubuntu Runner
          ↓
 ┌─────────────────────┐
 │ Python              │
 │ Node.js              │
 │ Appium               │
 │ Android SDK          │
 │ Android Emulator     │
 └─────────────────────┘
          ↓
      pytest
          ↓
 ┌────────┼───────────┐
 ↓        ↓           ↓
HTML     Logs      Screenshots
Report
          ↓
   GitHub Artifacts


Local Framework
      ↓
GitHub Actions
      ↓
Android SDK
      ↓
AVD
      ↓
KVM
      ↓
Android Emulator
      ↓
ADB
      ↓
Appium Server
      ↓
UiAutomator2
      ↓
Pytest
      ↓
🎉 MOBILE TESTS RUNNING IN CI