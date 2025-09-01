prompt = """
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