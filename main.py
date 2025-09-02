import os
import json
from typing import Dict, Any
from langchain.prompts import PromptTemplate
from parser.json_output_parser import JSONOutputParser
from processor.document_processor import DocumentProcessor
# from parser.json_to_excel_parser import json_to_excel
from parser.json_to_xlsx_parser import json_to_excel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
# from template.prompt_template import prompt
from template.prompt_template_new import prompt

load_dotenv()

class ProjectEstimationSystem:
    """Main system for generating project estimations from documents"""
    
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        """Initialize the system with Groq LLM"""
        try:
            self.model = model
            self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name=model, temperature=0.3)
            self.output_parser = JSONOutputParser()
            self.doc_processor = DocumentProcessor()
            print(f"Initialized with model: {model}")
        except Exception as e:
            raise Exception(f"Failed to initialize Groq model '{model}': {e}")
        
        # Create a more focused prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["document_content"],
            template=prompt
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
            
            # Generate estimation with retry mechanism
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    print(f"Attempt {attempt + 1}: Generating estimation...")
                    
                    # Generate prompt
                    formatted_prompt = self.prompt_template.format(document_content=document_content)
                    
                    # Save prompt to a text file
                    if(os.getenv("DEBUG").lower() == "true"):
                        with open("prompt.txt", "w", encoding="utf-8") as f:
                            f.write(formatted_prompt)
                    
                    # Get LLM response
                    response = self.llm.invoke(formatted_prompt)
                
                    if not response or len(response.content.strip()) < 10:
                        raise ValueError("Empty or too short response from LLM")
                    
                    print(f"Received response, length: {len(response.content)} characters")
                    if(os.getenv("DEBUG").lower() == "true"):
                        with open("response.txt", "w", encoding="utf-8") as ff:
                            ff.write(response.content)
                        
                    # Parse JSON response
                    estimation_data = self.output_parser.parse(response.content)
                    
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
            
            
            
            return {}
            
        except Exception as e:
            print(f"Critical error in processing: {str(e)}")
            raise Exception(f"Error processing document: {e}")
    
    def _validate_estimation_structure(self, data: Dict[str, Any]) -> bool:
        """Validate that the estimation data has required structure for new format"""
        try:
            # Check required top-level keys
            required_keys = ['projectInfo', 'phases']
            for key in required_keys:
                if key not in data:
                    print(f"Missing required key: {key}")
                    return False
            
            # Check project info structure
            project_info = data['projectInfo']
            project_info_keys = ['title', 'projectName']
            for key in project_info_keys:
                if key not in project_info:
                    print(f"Missing projectInfo key: {key}")
                    return False
            
            # Check phases structure
            phases = data['phases']
            if not isinstance(phases, list):
                print("Phases must be a list")
                return False
            
            if len(phases) == 0:
                print("At least one phase is required")
                return False
            
            # Validate phase structure
            for i, phase in enumerate(phases):
                if not isinstance(phase, dict):
                    print(f"Phase {i} must be a dictionary")
                    return False
                
                phase_keys = ['name', 'tasks']
                for key in phase_keys:
                    if key not in phase:
                        print(f"Missing phase key: {key}")
                        return False
                
                # Validate tasks in phase
                tasks = phase['tasks']
                if not isinstance(tasks, list):
                    print(f"Tasks in phase {i} must be a list")
                    return False
                
                # Validate at least one task if tasks exist
                if tasks:
                    first_task = tasks[0]
                    task_keys = ['taskName', 'resource', 'minHours', 'maxHours', 'status']
                    for key in task_keys:
                        if key not in first_task:
                            print(f"Missing task key: {key}")
                            return False
                    
                    # Validate hours are numbers
                    min_hours = first_task.get('minHours')
                    max_hours = first_task.get('maxHours')
                    
                    if min_hours is not None and max_hours is not None:
                        try:
                            min_val = float(min_hours) if isinstance(min_hours, str) else min_hours
                            max_val = float(max_hours) if isinstance(max_hours, str) else max_hours
                            
                            if min_val < 0 or max_val < 0:
                                print("Hours must be non-negative")
                                return False
                            
                            if min_val > max_val:
                                print("Min hours cannot be greater than max hours")
                                return False
                        except (ValueError, TypeError):
                            print("Hours must be valid numbers")
                            return False
            
            return True
            
        except Exception as e:
            print(f"Validation error: {e}")
            return False

      
    def save_estimation(self, estimation_data: Dict[str, Any], output_path: str):
        """Save estimation data to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(estimation_data, f, indent=2, ensure_ascii=False)
            print(f"✓ Estimation saved to: {output_path}")
        except Exception as e:
            raise Exception(f"Error saving estimation: {e}")


def main():
    """Main function with comprehensive error handling"""
    print("=" * 60)
    print("PROJECT ESTIMATION SYSTEM")
    print("=" * 60)
    
    # Configuration
    DOCUMENT_PATH = os.getenv("DOCUMENT_PATH", "sampleproject.pdf")  # Update this path
    OUTPUT_PATH = os.getenv("OUTPUT_PATH", "project_estimation.json")
    MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    
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
        estimation_system = ProjectEstimationSystem(model=MODEL)
        
        print("\n4. Processing document and generating estimation...")
        estimation_data = estimation_system.process_document_and_estimate(DOCUMENT_PATH)
        
        print("\n5. Saving results to JSON...")
        estimation_system.save_estimation(estimation_data, OUTPUT_PATH)
        
        print("\n6. Converting to Excel...")
        json_to_excel(estimation_data, "estimation_data.xlsx")
        
        print("\n7. Done!")
        
        # Step 4: Display summary
        print("\n" + "=" * 60)
        print("PROJECT ESTIMATION SUMMARY")
        print("=" * 60)
        
        project_info = estimation_data.get('projectInfo', {})
        summary = estimation_data.get('summary', {})
        phases = estimation_data.get('phases', [])
        
        print(f"Project Title: {project_info.get('title', 'N/A')}")
        print(f"Project Name: {project_info.get('projectName', 'N/A')}")
        print(f"Client: {project_info.get('client', 'N/A')}")
        print(f"Date: {project_info.get('date', 'N/A')}")
        print(f"Version: {project_info.get('version', 'N/A')}")
        print(f"Prepared By: {project_info.get('preparedBy', 'N/A')}")
        
        if summary:
            print(f"Estimated Hours: {summary.get('totalMinHours', 0)} - {summary.get('totalMaxHours', 0)}")
            print(f"Duration: {summary.get('estimatedDurationWeeks', 0)} weeks")
            print(f"Team Size: {summary.get('recommendedTeamSize', 0)} people")
            print(f"Total Tasks: {summary.get('totalTasks', 0)}")
            print(f"Total Phases: {summary.get('totalPhases', len(phases))}")
        else:
            # Calculate summary from phases if not provided
            total_min_hours = 0
            total_max_hours = 0
            total_tasks = 0
            
            for phase in phases:
                for task in phase.get('tasks', []):
                    try:
                        min_hours = float(task.get('minHours', 0))
                        max_hours = float(task.get('maxHours', 0))
                        total_min_hours += min_hours
                        total_max_hours += max_hours
                        total_tasks += 1
                    except (ValueError, TypeError):
                        continue
            
            print(f"Estimated Hours: {total_min_hours} - {total_max_hours}")
            print(f"Total Tasks: {total_tasks}")
            print(f"Total Phases: {len(phases)}")
        
        print(f"\n✓ Complete estimation saved to: {OUTPUT_PATH}")
        print("\nYou can now review the detailed JSON estimation file.")
        
    except Exception as e:
        print(f"\n✗ Error during processing: {e}")
        print("\nIf the error persists, try:")
        print("- Using a smaller/simpler document")
        print("- Checking your Groq API key")
        print("- Verifying the document format is supported")

if __name__ == "__main__":
    main()