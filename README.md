# GRC News Assistant

A Python-based tool for collecting and analyzing GRC (Governance, Risk, and Compliance) related news articles using NewsData.io API and AI-powered analysis.

## Prerequisites

Before using this tool, ensure you have the following prerequisites installed:

1. Python 3.7 or higher
2. [fabric](https://github.com/danielmiessler/fabric) - Must be installed separately
3. OS-specific clipboard tools:
   - macOS: Built-in use of pbpaste, no additional installation needed
   - Linux: Install xclip
     ```bash
     # Ubuntu/Debian
     sudo apt-get install xclip
     
     # Fedora
     sudo dnf install xclip
     ```
   - Windows: Built-in PowerShell commands used, no additional installation needed

## Installation

1. Clone this repository or download the files
   ```
   git clone https://github.com/cpatocybersecurity/GRCnewsAssistant
   ```
3. Go to the GRCnewsAssistant directory
   ```bash
   cd GRCnewsAssistant
   ```
4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Set up NLTK data:
   ```python
   python -c "import nltk; nltk.download('punkt')"
   ```

## API Key Setup

This tool requires a NewsData.io API key. Follow these steps to set it up:

1. Sign up for a free account at [NewsData.io](https://newsdata.io)
2. Get your API key from the dashboard
3. Set your API key as an environment variable:

   For macOS/Linux:
   ```bash
   export NEWSDATA_API_KEY='your_api_key_here'
   ```
   Add this line to your shell's startup file (.bashrc, .zshrc, etc.) to make it permanent.

   For Windows (Command Prompt):
   ```cmd
   set NEWSDATA_API_KEY=your_api_key_here
   ```

   For Windows (PowerShell):
   ```powershell
   $env:NEWSDATA_API_KEY='your_api_key_here'
   ```

## Usage

1. Prepare your keywords:
   - Modify the file named `keywords.csv` in the same directory as the script
   - Modify or add one keyword per line
   - Use "%20" where any spaces would be, e.g. "cybersecutiy%20GRC"

2. Run the script:
   ```bash
   python GRCnewsAssistant.py
   ```

The script will:
- Search for news articles matching your keywords
- Save the initial results to `grcdata.csv`
- Extract article content and perform AI analysis using the label_and_rate pattern/prompt from fabric (or you can modify how ratings are determined with a custom fabric pattern)
- Save the analyzed results to `grcdata_rated.csv`

## Output Files

- `grcdata.csv`: Raw article data including dates, keywords, titles, descriptions, and URLs
- `urls.csv`: List of article URLs for easy reference (and automated input to the NP4k-extractor service while you run GRCnewsAssistant.py
- `grcdata_rated.csv`: Enhanced dataset including AI analysis results

## Error Handling

The script includes comprehensive error handling and will provide clear messages if:
- The API key is not set
- Required clipboard tools are missing (Linux)
- Keywords file is missing or empty
- API requests fail
- Article processing encounters issues

## Operating System Compatibility

The script is compatible with:
- macOS (uses built-in pbcopy/pbpaste)
- Linux (requires xclip)
- Windows (uses PowerShell's Get-Clipboard)

## Troubleshooting

1. **API Key Issues**
   - Ensure the environment variable is set correctly
   - Check if your API key is valid at NewsData.io

2. **Linux Clipboard Issues**
   - Verify xclip is installed: `which xclip`
   - Try reinstalling xclip if needed

3. **Windows PowerShell Issues**
   - Ensure you're running with appropriate permissions
   - Try running PowerShell as administrator if needed

## Credits

This project builds upon the work of several excellent open-source projects:

- [grcAssist](https://github.com/gerryguy311/grcAssist) by Dr. Gerald Auger - The original GRC news assistant that inspired this AI-enhanced version
- [fabric](https://github.com/danielmiessler/fabric) by Daniel Miessler - Provides the AI-powered analysis capabilities
- [NP4k-extractor](https://github.com/nopslip/NP4k-extractor) by nopslip - Influenced the article extraction and processing workflow

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
