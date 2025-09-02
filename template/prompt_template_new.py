prompt = """
You are an expert software project manager and technical lead with extensive experience in project estimation and planning. Analyze the following project specification document and provide a detailed breakdown with accurate estimations organized by project phases.

DOCUMENT:
{document_content}

INSTRUCTIONS:
1. Carefully read and understand the entire project specification
2. Identify all major features, modules, and components
3. Break down the project into logical phases and tasks within each phase
4. Organize tasks according to standard software development phases
5. Provide realistic time estimations based on industry standards
6. Consider technical complexity, dependencies, and potential risks
7. Include all necessary skills and expertise required for each task

ESTIMATION CRITERIA:
- Use person-hours for all estimates
- Min hours: Optimistic scenario (best case)
- Max hours: Pessimistic scenario including potential issues
- Consider technical complexity and dependencies
- Include specific resources/skills required for each task
- Provide realistic start and end dates
- Set appropriate task status

PHASES TO CONSIDER:
- Design & Architecture Phase: UI/UX design, system architecture, technical specifications
- General Phase: Project setup, basic configurations, common utilities
- Testing & QA Phase: Test setup, quality assurance, bug fixing
- Development Phase: Core feature development, integrations, APIs
- Planning & Analysis Phase: Requirements analysis, workflow design, user journey mapping
- Documentation Phase: Technical documentation, user guides, API documentation
- Performance Phase: Optimization, performance monitoring, scaling
- Deployment & DevOps Phase: CI/CD setup, deployment, server configuration
- Project Management Phase: Project coordination, reviews, management tasks
- Database Phase: Database design, migrations, data management

Return your response as a valid JSON object with the following structure:

{{
  "projectInfo": {{
    "title": "Title of project or application",
    "projectName": "Name of project or application", 
    "client": "Client name if specified",
    "date": "Current date (YYYY-MM-DD)",
    "version": "1.0",
    "preparedBy": "Your name or team",
    "assumptions": "Key global assumptions for the project"
  }},
  "phases": [
    {{
      "name": "DESIGN & ARCHITECTURE PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task (e.g., UI Designer, Backend Developer)",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task", 
          "startDate": "Start date of task (YYYY-MM-DD)",
          "endDate": "End date of task (YYYY-MM-DD)",
          "status": "Not Started/In Progress/Completed"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "GENERAL PHASE", 
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task", 
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "TESTING & QA PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task", 
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "DEVELOPMENT PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task", 
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "PLANNING & ANALYSIS PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task", 
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "DOCUMENTATION PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": "Documentation Subtotal"
    }},
    {{
      "name": "PERFORMANCE PHASE", 
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "DEPLOYMENT & DEVOPS PHASE",
      "tasks": [
        {{
          "taskName": "Name of task", 
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "PROJECT MANAGEMENT PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task",
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
    {{
      "name": "DATABASE PHASE",
      "tasks": [
        {{
          "taskName": "Name of task",
          "resource": "Resource required for task", 
          "minHours": "Minimum hours required for task",
          "maxHours": "Maximum hours required for task",
          "startDate": "Start date of task",
          "endDate": "End date of task",
          "status": "Status of task"
        }},
        ...
      ],
      "subtotal": {{
        "minHours": "Minimum hours required for phase",
        "maxHours": "Maximum hours required for phase"
      }}
    }},
  ],
  "grandTotal": "Grand Total",
  "summary": {{ 
    "totalMinHours": 0,
    "totalMaxHours": 0,
    "estimatedDurationWeeks": 0,
    "recommendedTeamSize": 0,
    "totalTasks": 0,
    "totalPhases": 10
  }},
  "risks": [
    {{
      "risk": "Risk description",
      "phase": "Affected phase",
      "impact": "High/Medium/Low", 
      "mitigation": "Mitigation strategy"
    }},
    ...
  ],
  "recommendations": [
    "Recommendation 1",
    "Recommendation 2",
    ...
  ]
}}

IMPORTANT GUIDELINES:
- Ensure all tasks are categorized into appropriate phases
- Provide realistic min/max hour estimates for each task
- Include specific resource requirements (roles/skills needed)
- Set realistic start and end dates based on dependencies
- All tasks should initially have "Not Started" status unless specified otherwise
- Consider dependencies between phases and tasks
- Include comprehensive risk assessment and mitigation strategies
- Ensure estimates are based on actual project requirements specified in the document
- Be thorough and consider all aspects: analysis, design, development, testing, deployment, and documentation
"""