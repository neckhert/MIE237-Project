# MIE237 Project: How well can humans discern AI-generated and Real content

This project is a Tkinter-based application designed to test the hypothesis of human ability to discern AI-generated and real content. Users view videos and audio clips through a series of interfaces and cast their votes.

## Project Structure

```
MIE237-Project
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui
│   │   ├── consent_window.py   # Consent window implementation
│   │   ├── test_interface.py   # Test interface for video playback and voting
│   │   └── __init__.py         # UI package initializer
│   ├── data
│   │   ├── database.py         # Database interaction functions
│   │   ├── csv_handler.py      # CSV file handling functions
│   │   └── __init__.py         # Data package initializer
│   └── utils
│       ├── video_player.py     # Video playback management
│       └── __init__.py         # Utils package initializer
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd tkinter-voting-app
   ```

2. **Install dependencies**:
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**:
   Execute the main script:
   ```
   python src/main.py
   ```

## Usage Guidelines

- Upon launching the application, users will first see a consent window.
- After consenting, users will be directed to the test interface where they are given the test and cast their votes.
- Users need to enter their ID or name, which will be recorded along with their voting data.
- The application supports data submission to both CSV files and databases, making it easy to access and analyze the voting data.
