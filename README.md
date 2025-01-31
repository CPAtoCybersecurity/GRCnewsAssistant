# GRC News Assistant

This Python-based tool requires minimial coding experience for users to collect and analyze Cybersecurity GRC (Governance, Risk, and Compliance) related news articles (or any topic of interest) using NewsData.io API, with AI provided ratings powered by fabric.  You just add a few keywords into a csv file, run the script (e.g. daily), and it adds news articles to a spreadsheet, with ratings from "S Tier: (Must Consume Original Content Immediately)" to "C Tier (Maybe Skip It)."  This capability provides GRC professionals with a bank of quick-to-access relevant cyber news stories to help win hearts and minds for cyber risk reduction with executives, managers, IT practitioners and end users.

This project is inspired by and builds upon the work of several excellent open-source projects:

- [grcAssist by Dr. Gerald Auger - The original GRC news assistant](https://github.com/gerryguy311/grcAssist)
- [fabric by Daniel Miessler - Provides the AI-powered analysis capabilities with the label_and_rate pattern/prompt](https://github.com/danielmiessler/fabric)
- [NP4k-extractor by nopslip - URL to fabric processing](https://github.com/nopslip/NP4k-extractor)

## Related Videos

- [Simply Cyber - Is Manual GRC REALLY Slowing You Down? Automate NOW!](https://www.youtube.com/watch?v=IfX6CMi-bpI)
- [CPA to Cybersecurity - Fabric Client Installation: Your Personal AI Ecosystem](https://youtu.be/1csePKEwDY0)
- [Unsupervised Learning - Introducing Fabric — A Human AI Augmentation Framework](https://www.youtube.com/watch?v=wPEyyigh10g)

## Prerequisites

Before using this tool, ensure you have the following prerequisites installed:

1. Python 3.7 or higher
   ```bash
   #Check python version
   python3 --version
   ```
3. [fabric](https://github.com/danielmiessler/fabric) - Must be installed separately. I have a step-by-step blog post with a video walkthrough here: https://www.cpatocybersecurity.com/p/install-the-new-fabric
4. OS-specific clipboard tools:
   - macOS: Built-in with pbpaste, no additional installation needed
   - Linux: Install xclip
     ```bash
     # Ubuntu/Debian
     sudo apt-get install xclip
     
     # Fedora
     sudo dnf install xclip
     ```
   - Windows: Built-in PowerShell commands used, no additional installation needed

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/cpatocybersecurity/GRCnewsAssistant
   cd GRCnewsAssistant
   ```
2. Create and activate a virtual environment:
   ```
   # Create a virtual environment
   python3 -m venv venv

   # Activate it
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   .\venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```
   # With virtual environment activated:
   pip install -r requirements.txt
   ```
4. Set up NLTK data:
   ```
   # With virtual environment activated:
   python -c "import nltk; nltk.download('punkt')"
   ```

## API Key Setup

This tool requires a NewsData.io API key. Follow these steps to set it up:

1. Sign up for a free account at [NewsData.io](https://newsdata.io)
2. Get your API key from the dashboard
3. Set your API key as an environment variable:

   For macOS/Linux:
   ```bash
   #Edit your shell's startup file
   nano ~/.zshrc

   #add this line to your shell's startup file to make it permanent
   export NEWSDATA_API_KEY='your_api_key_here'
   
   #Or .bashrc, etc. depending on your environment
   ```
   
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
   - Modify the file named `keywords.csv` in the same directory as the script, with new items of interest
   - Add one keyword per line, or multiple words per line with "%20" in spaces between words 

2. Run the script:
   ```bash
   #Go to the grcnewsassistant directory if you're not already there
   cd grcnewsassistant

   #Activate the virtual enviornment if it's not already activated, e.g. for macOS/Linus:
   source venv/bin/activate

   # On Windows:
   .\venv\Scripts\activate

   #Execute the script   
   python GRCnewsAssistant.py
   ```

The script will:
- Search for news articles matching your keywords
- Save the initial results to `grcdata.csv`
- Extract article content and perform AI analysis using fabric
- Save the analyzed results to `grcdata_rated.csv`

## Output Files

- `grcdata.csv`: Raw article data including dates, keywords, titles, descriptions, and URLs
- `urls.csv`: List of article URLs for easy reference
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

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
 
