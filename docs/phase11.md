                    Ubuntu Host
              ┌─────────────────────┐
              │ Android Emulator    │
              │        ↑            │
              │     Appium          │
              │     :4723           │
              └─────────┬───────────┘
                        │
                  host network
                        │
              ┌─────────▼───────────┐
              │   Docker Container  │
              │                     │
              │ Python 3.12         │
              │ Dependencies        │
              │ Your Framework      │
              │ Pytest              │
              │                     │
              │ 8 tests             │
              │ 8 passed ✅         │
              └─────────────────────┘