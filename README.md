# Project Estimation System

An AI-powered project estimation tool that analyzes project specification documents and generates detailed project estimations with time breakdowns, resource requirements, and risk assessments. The system automatically converts estimations into professional Excel reports following industry-standard project estimation templates.

## Features

- **Document Analysis**: Supports PDF and DOCX project specification documents
- **AI-Powered Estimation**: Uses Groq's LLM models for intelligent project breakdown
- **Phase-Based Organization**: Organizes tasks across 10 standard software development phases
- **Excel Export**: Generates professional Excel reports with proper formatting
- **Comprehensive Output**: Includes project summary, risks, and recommendations
- **Flexible Configuration**: Environment-based configuration for easy customization

## Installation

### Prerequisites

- Python 3.8 or higher
- Groq API key (sign up at https://console.groq.com/)

### Setup

1. **Clone the repository**

   ```bash
   git clone <https://github.com/uxama-jamil/llm-project-estimator.git>
   cd llm-project-estimator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**

   Copy `.env.example` to `.env` and update with your settings:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```env
   GROQ_MODEL=openai/gpt-oss-20b
   GROQ_API_KEY=your_groq_api_key_here
   DOCUMENT_PATH=sampleproject.pdf
   OUTPUT_PATH=project_estimation.json
   DEBUG=false
   ```

## Usage

### Basic Usage

1. **Place your project document** in the root directory or specify the path in `.env`
2. **Run the estimation system**
   ```bash
   python main.py
   ```

The system will:

- Extract content from your document
- Generate detailed project estimation
- Save JSON output
- Create Excel report (`estimation_data.xlsx`)

### Output Files

- **`project_estimation.json`**: Raw JSON estimation data
- **`estimation_data.xlsx`**: Professional Excel report
- **`prompt.txt`** (if DEBUG=true): Generated prompt for debugging
- **`response.txt`** (if DEBUG=true): Raw LLM response for debugging

## Project Structure

```
project-estimation-system/
├── main.py                     # Main application entry point
├── requirements.txt            # Python dependencies
├── .env                       # Environment configuration
├── README.md                  # This file
├── template/
│   └── prompt_template_new.py # LLM prompt template
├── parser/
│   ├── json_output_parser.py  # JSON response parser
│   └── json_to_xlsx_parser.py # Excel export functionality
└── processor/
    └── document_processor.py  # Document content extraction
```

## Supported Document Formats

- **PDF** (`.pdf`): Text-based PDFs
- **Word Documents** (`.docx`, `.doc`): Microsoft Word files

## Excel Report Structure

The generated Excel report includes:

### Main Estimation Table

- **Project Information**: Name, client, date, version, assumptions
- **Phase-Based Tasks**: Organized across 10 development phases
- **Resource Requirements**: Specific roles and skills needed
- **Time Estimates**: Minimum and maximum hours for each task
- **Schedule**: Start and end dates
- **Status Tracking**: Task completion status

### Additional Sections

- **Project Summary**: Total hours, duration, team size
- **Risks & Considerations**: Identified risks with mitigation strategies
- **Recommendations**: Best practices and suggestions

### Phases Covered

1. Design & Architecture Phase
2. General Phase
3. Testing & QA Phase
4. Development Phase
5. Planning & Analysis Phase
6. Documentation Phase
7. Performance Phase
8. Deployment & DevOps Phase
9. Project Management Phase
10. Database Phase

## Configuration Options

### Environment Variables

| Variable        | Description              | Default                   |
| --------------- | ------------------------ | ------------------------- |
| `GROQ_MODEL`    | LLM model to use         | `openai/gpt-oss-20b`      |
| `GROQ_API_KEY`  | Your Groq API key        | Required                  |
| `DOCUMENT_PATH` | Path to input document   | `sampleproject.pdf`       |
| `OUTPUT_PATH`   | JSON output file path    | `project_estimation.json` |
| `DEBUG`         | Enable debug file output | `false`                   |

### Supported Models

The system supports various Groq models:

- `openai/gpt-oss-20b` (default)
- `meta-llama/llama-3.1-8b-instant`
- `meta-llama/llama-3.1-70b-versatile`
- And other Groq-supported models

## API Response Format

The system generates structured JSON with the following format:

```json
{
  "projectInfo": {
    "title": "Project Title",
    "projectName": "Project Name",
    "client": "Client Name",
    "date": "2025-01-01",
    "version": "1.0",
    "preparedBy": "Estimator Name",
    "assumptions": "Key assumptions"
  },
  "phases": [
    {
      "name": "PHASE NAME",
      "tasks": [
        {
          "taskName": "Task Name",
          "resource": "Required Resource",
          "minHours": 40,
          "maxHours": 60,
          "startDate": "2025-01-01",
          "endDate": "2025-01-05",
          "status": "Not Started"
        }
      ],
      "subtotal": {
        "minHours": 40,
        "maxHours": 60
      }
    }
  ],
  "summary": {
    "totalMinHours": 1000,
    "totalMaxHours": 1500,
    "estimatedDurationWeeks": 12,
    "recommendedTeamSize": 5,
    "totalTasks": 50,
    "totalPhases": 10
  },
  "risks": [...],
  "recommendations": [...]
}
```

## Troubleshooting

### Common Issues

1. **"Document not found"**

   - Verify the document path in `.env`
   - Ensure the file exists and has proper permissions

2. **"Empty or too short response from LLM"**

   - Check your Groq API key
   - Verify API quota and rate limits
   - Try a different model

3. **"Invalid JSON in response"**

   - Enable DEBUG mode to inspect raw responses
   - The system includes automatic JSON repair mechanisms
   - Complex documents may require multiple attempts

4. **Excel generation errors**
   - Ensure sufficient disk space
   - Check file permissions in output directory
   - Close Excel if the output file is open

### Debug Mode

Enable debug mode for troubleshooting:

```env
DEBUG=true
```

This creates additional files:

- `prompt.txt`: Generated prompt sent to LLM
- `response.txt`: Raw LLM response

## Dependencies

- **langchain**: LLM framework
- **langchain-groq**: Groq integration
- **PyPDF2**: PDF processing
- **python-docx**: Word document processing
- **pandas**: Data manipulation
- **openpyxl**: Excel file creation
- **python-dotenv**: Environment configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please:

1. Check the troubleshooting section
2. Review debug output if enabled
3. Open an issue with relevant error messages and system information

## Changelog

### v1.0.0

- Initial release
- Support for PDF and DOCX documents
- Groq LLM integration
- Excel report generation
- Phase-based project organization
- Risk and recommendation analysis
