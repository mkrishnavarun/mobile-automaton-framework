mobile-automation-framework/
├── reports/
│   ├── html/
│   │   └── report.html
│   └── screenshots/
├── logs/
│   └── framework.log
├── core/
├── pages/
├── tests/
└── utils/

What we have achieved
                 Every test
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
     Appium Driver          Log Capture
          │                     │
          ↓                     ↓
      Test actions          Test logs
          │                     │
          └──────────┬──────────┘
                     ↓
                Test result
                     │
                  Failure?
                  /      \
                Yes       No
                 ↓         ↓
            Screenshot    Done
                 +
              Logs
                 ↓
           HTML Report