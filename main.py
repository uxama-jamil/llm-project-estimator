import os
import json
from typing import Dict, Any
from langchain.prompts import PromptTemplate
from parser.json_output_parser import JSONOutputParser
from processor.document_processor import DocumentProcessor
from parser.json_to_excel_parser import json_to_excel
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from template.prompt_template import prompt

load_dotenv()

class ProjectEstimationSystem:
    """Main system for generating project estimations from documents"""
    
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        """Initialize the system with Ollama LLM"""
        try:
            self.model = model
            self.llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name=model, temperature=0.3)
            self.output_parser = JSONOutputParser()
            self.doc_processor = DocumentProcessor()
            print(f"Initialized with model: {model}")
        except Exception as e:
            raise Exception(f"Failed to initialize Ollama model '{model}': {e}")
        
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
                    
                    # Save prompt to a text file
                    with open("prompt.txt", "w", encoding="utf-8") as f:
                        f.write(prompt)
                    
                    # Get LLM response
                        response = self.llm.invoke(prompt)
                
                    if not response or len(response.content.strip()) < 10:
                        raise ValueError("Empty or too short response from LLM")
                    
                    print(f"Received response, length: {len(response.content)} characters")
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
            
            # Generate fallback if all attempts failed
            print("Generating fallback estimation...")
            return {}
            
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

if __name__ == "__main__":
    main()