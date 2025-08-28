import os
import json
from typing import Dict, Any
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from parser.json_output_parser import JSONOutputParser
from processor.document_processor import DocumentProcessor



class ProjectEstimationSystem:
    """Main system for generating project estimations from documents"""
    
    def __init__(self, ollama_model: str = "llama3.2"):
        """Initialize the system with Ollama LLM"""
        try:
            self.llm = Ollama(
                model=ollama_model,
                temperature=0.3,
                num_predict=4000
            )
            self.output_parser = JSONOutputParser()
            self.doc_processor = DocumentProcessor()
            print(f"Initialized with model: {ollama_model}")
        except Exception as e:
            raise Exception(f"Failed to initialize Ollama model '{ollama_model}': {e}")
        
        # Create a more focused prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["document_content"],
            template="""
     You are an expert software project manager and technical lead with extensive experience in project estimation and planning. Analyze the following project specification document and provide a detailed breakdown with accurate estimations.

    DOCUMENT:
    {document_content}

INSTRUCTIONS:
1. Carefully read and understand the entire project specification
2. Identify all major features, modules, and components
3. Break down the project into logical tasks and subtasks
4. Provide realistic time estimations based on industry standards
5. Consider technical complexity, dependencies, and potential risks
6. Include all necessary skills and expertise required

ESTIMATION CRITERIA:
- Use person-hours for all estimates
- Min hours: Optimistic scenario (best case)
- Max hours: Pessimistic scenario including potential issues
- Complexity scale: Low (1-2), Medium (3-4), High (5)
- Dependencies: Internal and external dependencies
- Skills: Specific technical skills required
- Assumptions: Key assumptions made for estimates

Return your response as a valid JSON object with the following structure:

{{
    "project_overview": {{
        "title": "Project Title",
        "description": "Brief project description",
        "total_min_hours": 0,
        "total_max_hours": 0,
        "estimated_duration_weeks": 0,
        "team_size_recommended": 0
    }},
    "tasks": [
        {{
            "task_id": "T001",
            "task_name": "Task Name",
            "description": "Detailed task description",
            "subtasks": [
                {{
                    "subtask_id": "ST001",
                    "subtask_name": "Subtask Name",
                    "description": "Subtask description",
                    "min_hours": 0,
                    "max_hours": 0,
                    "skills_required": ["skill1", "skill2"],
                    "complexity": 0,
                    "dependencies": ["dependency1", "dependency2",...],
                    "assumptions": ["assumption1", "assumption2",...]
                }}
            ],
            "task_total_min_hours": 0,
            "task_total_max_hours": 0,
            "critical_path": false
        }}
    ],
    "risks_and_considerations": [
        {{
            "risk": "Risk description",
            "impact": "High/Medium/Low",
            "mitigation": "Mitigation strategy"
        }},...
    ],
    "resource_requirements": {{
        "skills_summary": {{
            "skill_name": "hours_required",...
        }},
        "team_composition": [
            {{
                "role": "Role name",
                "skills": ["skill1", "skill2",...],
                "estimated_hours": 0
            }},...
        ]
    }},
    "assumptions": [
        "Global assumption 1",
        "Global assumption 2",
        ...
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        ...
    ]
}}

Ensure all estimates are realistic and based on the actual requirements specified in the document. Be thorough and consider all aspects of software development including analysis, design, development, testing, deployment, and documentation."""
        )
    
    def process_document_and_estimate(self, file_path: str) -> Dict[str, Any]:
        """Process document and generate project estimation"""
        try:
            # Extract document content
            print(f"Extracting content from: {file_path}")
            document_content = self.doc_processor.extract_content(file_path)
            
            if not document_content.strip():
                raise ValueError("No content extracted from document")
            
            print(f"Document content extracted: {len(document_content)} characters")
            
            # Truncate content if too long
            # max_content_length = 6000
            # if len(document_content) > max_content_length:
            #     print(f"Document too long, truncating to {max_content_length} characters")
            #     document_content = document_content[:max_content_length] + "\n\n[Document truncated for processing]"
            
            # Generate estimation with retry mechanism
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1}: Generating estimation...")
                    
                    # Generate prompt
                    prompt = self.prompt_template.format(document_content=document_content)
                    
                    # Get LLM response
                    response = self.llm.invoke(prompt)
                    
                    if not response or len(response.strip()) < 10:
                        raise ValueError("Empty or too short response from LLM")
                    
                    print(f"Received response, length: {len(response)} characters")
                    
                    # Parse JSON response
                    estimation_data = self.output_parser.parse(response)
                    
                    # Validate the parsed data
                    if self._validate_estimation_structure(estimation_data):
                        print("✓ Estimation data validated successfully")
                        return estimation_data
                    else:
                        print("✗ Invalid estimation data structure")
                        if attempt == max_retries - 1:
                            print("All validation attempts failed, using fallback")
                            break
                        continue
                        
                except Exception as e:
                    print(f"Attempt {attempt + 1} failed: {str(e)}")
                    if attempt == max_retries - 1:
                        print("All LLM attempts failed, generating fallback response")
                        break
                    print("Retrying...")
                    continue
            
            # Generate fallback if all attempts failed
            print("Generating fallback estimation...")
            return self._generate_fallback_estimation(document_content)
            
        except Exception as e:
            print(f"Critical error in processing: {str(e)}")
            raise Exception(f"Error processing document: {e}")
    
    def _validate_estimation_structure(self, data: Dict[str, Any]) -> bool:
        """Validate that the estimation data has required structure"""
        try:
            # Check required top-level keys
            required_keys = ['project_overview', 'tasks']
            for key in required_keys:
                if key not in data:
                    print(f"Missing required key: {key}")
                    return False
            
            # Check project overview structure
            overview = data['project_overview']
            overview_keys = ['title', 'total_min_hours', 'total_max_hours']
            for key in overview_keys:
                if key not in overview:
                    print(f"Missing project_overview key: {key}")
                    return False
            
            # Check that hours are valid numbers
            min_hours = overview.get('total_min_hours', 0)
            max_hours = overview.get('total_max_hours', 0)
            
            if not isinstance(min_hours, (int, float)) or not isinstance(max_hours, (int, float)):
                print("Hours must be numbers")
                return False
            
            if min_hours <= 0 or max_hours <= 0:
                print("Hours must be positive")
                return False
            
            if min_hours > max_hours:
                print("Min hours cannot be greater than max hours")
                return False
            
            # Check tasks structure
            tasks = data['tasks']
            if not isinstance(tasks, list):
                print("Tasks must be a list")
                return False
            
            if len(tasks) == 0:
                print("At least one task is required")
                return False
            
            # Validate at least the first task structure
            first_task = tasks[0]
            task_keys = ['task_name', 'subtasks']
            for key in task_keys:
                if key not in first_task:
                    print(f"Missing task key: {key}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Validation error: {e}")
            return False
    
    def _generate_fallback_estimation(self, document_content: str) -> Dict[str, Any]:
        """Generate a basic fallback estimation if LLM fails"""
        print("Generating fallback estimation based on document analysis...")
        
        # Simple content analysis
        word_count = len(document_content.split())
        lines = len(document_content.split('\n'))
        
        # Basic complexity estimation
        complexity_indicators = ['api', 'database', 'authentication', 'payment', 'integration', 
                               'mobile', 'web', 'frontend', 'backend', 'microservice']
        
        complexity_score = sum(1 for indicator in complexity_indicators 
                             if indicator.lower() in document_content.lower())
        
        # Calculate base hours (minimum 40, scale with content and complexity)
        base_hours = max(40, (word_count // 20) + (complexity_score * 10))
        min_hours = base_hours
        max_hours = int(base_hours * 1.6)  # 60% buffer
        
        # Estimate duration and team size
        duration_weeks = max(2, base_hours // 40)
        team_size = max(1, base_hours // 120)
        
        return {
            "project_overview": {
                "title": "Software Development Project (Auto-generated)",
                "description": f"Project estimation based on document analysis. Document contains {word_count} words with complexity score {complexity_score}.",
                "total_min_hours": min_hours,
                "total_max_hours": max_hours,
                "estimated_duration_weeks": duration_weeks,
                "team_size_recommended": team_size
            },
            "tasks": [
                {
                    "task_id": "T001",
                    "task_name": "Project Planning & Requirements",
                    "description": "Initial planning and requirements gathering phase",
                    "subtasks": [
                        {
                            "subtask_id": "ST001",
                            "subtask_name": "Requirements Analysis",
                            "description": "Analyze and document project requirements",
                            "min_hours": 16,
                            "max_hours": 24,
                            "skills_required": ["Business Analysis", "Documentation"],
                            "complexity": 2,
                            "dependencies": ["Stakeholder availability"],
                            "assumptions": ["Requirements are accessible"]
                        }
                    ],
                    "task_total_min_hours": 16,
                    "task_total_max_hours": 24,
                    "critical_path": True
                },
                {
                    "task_id": "T002",
                    "task_name": "Development",
                    "description": "Core development activities",
                    "subtasks": [
                        {
                            "subtask_id": "ST002",
                            "subtask_name": "Core Implementation",
                            "description": "Implement main functionality",
                            "min_hours": min_hours - 32,
                            "max_hours": max_hours - 48,
                            "skills_required": ["Programming", "Software Development"],
                            "complexity": 4,
                            "dependencies": ["Requirements completion", "Environment setup"],
                            "assumptions": ["Development tools available"]
                        }
                    ],
                    "task_total_min_hours": min_hours - 32,
                    "task_total_max_hours": max_hours - 48,
                    "critical_path": True
                },
                {
                    "task_id": "T003",
                    "task_name": "Testing & Deployment",
                    "description": "Quality assurance and deployment",
                    "subtasks": [
                        {
                            "subtask_id": "ST003",
                            "subtask_name": "Testing & QA",
                            "description": "Test application and ensure quality",
                            "min_hours": 16,
                            "max_hours": 24,
                            "skills_required": ["Testing", "QA"],
                            "complexity": 3,
                            "dependencies": ["Development completion"],
                            "assumptions": ["Test environment ready"]
                        }
                    ],
                    "task_total_min_hours": 16,
                    "task_total_max_hours": 24,
                    "critical_path": False
                }
            ],
            "risks_and_considerations": [
                {
                    "risk": "Requirements may be incomplete or unclear",
                    "impact": "Medium",
                    "mitigation": "Schedule regular stakeholder reviews and clarification sessions"
                },
                {
                    "risk": "Technical complexity may be underestimated",
                    "impact": "High",
                    "mitigation": "Include technical spikes and proof of concepts in planning"
                }
            ],
            "resource_requirements": {
                "skills_summary": {
                    "Business Analysis": 24,
                    "Software Development": max_hours - 48,
                    "Testing": 24,
                    "Project Management": 16
                },
                "team_composition": [
                    {
                        "role": "Business Analyst",
                        "skills": ["Business Analysis", "Documentation"],
                        "estimated_hours": 24
                    },
                    {
                        "role": "Software Developer",
                        "skills": ["Programming", "Software Development"],
                        "estimated_hours": max_hours - 48
                    },
                    {
                        "role": "QA Tester",
                        "skills": ["Testing", "QA"],
                        "estimated_hours": 24
                    }
                ]
            },
            "assumptions": [
                "Development environment and tools are available",
                "Team members have required technical skills",
                "Stakeholders are available for regular reviews",
                "No major changes to requirements during development"
            ],
            "recommendations": [
                "Conduct detailed requirements gathering before starting development",
                "Plan for regular progress reviews and stakeholder feedback",
                "Include buffer time for unforeseen technical challenges",
                "Establish clear communication channels with all stakeholders"
            ]
        }
    
    def save_estimation(self, estimation_data: Dict[str, Any], output_path: str):
        """Save estimation data to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(estimation_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Estimation saved to: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving estimation: {e}")

def test_ollama_connection(model_name: str = "llama3.2") -> bool:
    """Test if Ollama is working and model is available"""
    try:
        print(f"Testing connection to Ollama model: {model_name}")
        llm = Ollama(model=model_name, temperature=0.1)
        
        # Simple test
        response = llm.invoke("Say 'Hello' in JSON format like {\"message\": \"Hello\"}")
        print(f"Test response: {response}")
        
        if "hello" in response.lower() or "Hello" in response:
            print("✓ Ollama connection successful")
            return True
        else:
            print("⚠ Ollama responded but format unexpected")
            return False
            
    except Exception as e:
        print(f"✗ Ollama connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Start Ollama: ollama serve")
        print(f"2. Check if model exists: ollama list")
        print(f"3. Install model if needed: ollama pull {model_name}")
        return False

def main():
    """Main function with comprehensive error handling"""
    print("=" * 60)
    print("PROJECT ESTIMATION SYSTEM")
    print("=" * 60)
    
    # Configuration
    DOCUMENT_PATH = "sampleproject.pdf"  # Update this path
    OUTPUT_PATH = "project_estimation.json"
    OLLAMA_MODEL = "llama3.2:3b"
    
    # # Step 1: Test Ollama connection
    # print("\n1. Testing Ollama connection...")
    # if not test_ollama_connection(OLLAMA_MODEL):
    #     print("Please fix Ollama setup before continuing.")
    #     return
    
    # Step 2: Check if document exists
    print(f"\n2. Checking document: {DOCUMENT_PATH}")
    if not os.path.exists(DOCUMENT_PATH):
        print(f"✗ Document not found: {DOCUMENT_PATH}")
        print("Please update DOCUMENT_PATH variable with your actual document file path.")
        print("Supported formats: PDF (.pdf), Word (.docx, .doc)")
        return
    else:
        print(f"✓ Document found: {DOCUMENT_PATH}")
    
    # Step 3: Process document
    try:
        print("\n3. Initializing estimation system...")
        estimation_system = ProjectEstimationSystem(ollama_model=OLLAMA_MODEL)
        
        print("\n4. Processing document and generating estimation...")
        estimation_data = estimation_system.process_document_and_estimate(DOCUMENT_PATH)
        
        print("\n5. Saving results...")
        estimation_system.save_estimation(estimation_data, OUTPUT_PATH)
        
        # Step 4: Display summary
        print("\n" + "=" * 60)
        print("PROJECT ESTIMATION SUMMARY")
        print("=" * 60)
        
        overview = estimation_data.get('project_overview', {})
        print(f"Project Title: {overview.get('title', 'N/A')}")
        print(f"Description: {overview.get('description', 'N/A')}")
        print(f"Estimated Hours: {overview.get('total_min_hours', 0)} - {overview.get('total_max_hours', 0)}")
        print(f"Duration: {overview.get('estimated_duration_weeks', 0)} weeks")
        print(f"Team Size: {overview.get('team_size_recommended', 0)} people")
        print(f"Number of Tasks: {len(estimation_data.get('tasks', []))}")
        
        print(f"\n✓ Complete estimation saved to: {OUTPUT_PATH}")
        print("\nYou can now review the detailed JSON estimation file.")
        
    except Exception as e:
        print(f"\n✗ Error during processing: {e}")
        print("\nIf the error persists, try:")
        print("- Using a smaller/simpler document")
        print("- Checking if the document is readable")
        print("- Restarting Ollama service")

if __name__ == "__main__":
    print("Required packages: pip install langchain langchain-community PyPDF2 python-docx")
    print()
    main()