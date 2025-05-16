# Expense Tracker

A simple application to track your expenses and manage your budget.

## Features

- Add, edit, and delete expenses
- Categorize expenses
- View expense summaries and reports

## Installation

```bash
git clone https://github.com/binson-b/exp_tracker.git
cd exp_tracker


# Follow the detailed setup instructions in the [Setup Guide](https://github.com/binson-b/exp_tracker/wiki/Setup-Guide)
### On Discord
1. Create a bot on discord
2. Invite it to your server
3. get token

### On Google
1. Create a service account
2. Add that service account as a collaborator to your Google Sheet:
   - Open your Google Sheet.
   - Click on "Share" in the top-right corner.
   - Click "Send" to grant access.
3. Get API keys


### On server
1. run `./setup_server.sh`
2. Create a virtual environment using "virtualenv" or "venv":
   ```bash
   python3 -m venv env
   source env/bin/activate
3. Install all required dependencies:
   ```bash
   uv pip install -r requirements.txt

4. Run the `example_bot.py` script to start the bot. This script connects to Discord, Google Sheets, and Ollama services. Ensure you have set up the required API keys and tokens as described above:
   ```bash
   python example_bot.py
   ```


## Usage

1. Run the application.
2. Add your expenses.
3. Monitor your spending.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.