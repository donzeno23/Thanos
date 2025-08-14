from typing import Dict, List, Callable
from dataclasses import dataclass

from thanos.stages.login import login_to_service
from thanos.stages.user import create_user, check_user_profile
from thanos.stages.cleanup import cleanup_data
from .base_test_suite import StageDefinition


class StageFactory:
    """Factory for creating common stage definitions"""
    
    @staticmethod
    def create_login_stage() -> StageDefinition:
        """Create login stage definition"""
        return StageDefinition(
            name="login_to_service",
            action=login_to_service,
            dependencies=[]
        )
    
    @staticmethod
    def create_user_creation_stage() -> StageDefinition:
        """Create user creation stage definition"""
        return StageDefinition(
            name="create_user",
            action=create_user,
            dependencies=["login_to_service"],
            failure_condition=lambda params: params.get("rate") == 4
        )
    
    @staticmethod
    def create_user_check_stage() -> StageDefinition:
        """Create user profile check stage definition"""
        return StageDefinition(
            name="check_user_profile",
            action=check_user_profile,
            dependencies=["create_user"]
        )
    
    @staticmethod
    def create_cleanup_stage() -> StageDefinition:
        """Create cleanup stage definition"""
        return StageDefinition(
            name="cleanup_data",
            action=cleanup_data,
            dependencies=["create_user"]
        )
    
    @staticmethod
    def create_standard_workflow() -> List[StageDefinition]:
        """Create the standard workflow used by most test suites"""
        return [
            StageFactory.create_login_stage(),
            StageFactory.create_user_creation_stage(),
            StageFactory.create_user_check_stage(),
            StageFactory.create_cleanup_stage()
        ]


@dataclass
class WorkflowTemplate:
    """Template for different workflow configurations"""
    name: str
    stages: List[StageDefinition]
    description: str = ""


class WorkflowTemplateRegistry:
    """Registry for managing workflow templates"""
    
    _templates: Dict[str, WorkflowTemplate] = {}
    
    @classmethod
    def register_template(cls, template: WorkflowTemplate):
        """Register a workflow template"""
        cls._templates[template.name] = template
    
    @classmethod
    def get_template(cls, name: str) -> WorkflowTemplate:
        """Get a workflow template by name"""
        if name not in cls._templates:
            raise ValueError(f"Template '{name}' not found")
        return cls._templates[name]
    
    @classmethod
    def list_templates(cls) -> List[str]:
        """List all available template names"""
        return list(cls._templates.keys())


# Register standard templates
WorkflowTemplateRegistry.register_template(
    WorkflowTemplate(
        name="standard_user_workflow",
        stages=StageFactory.create_standard_workflow(),
        description="Standard workflow: login -> create user -> check profile -> cleanup"
    )
)

WorkflowTemplateRegistry.register_template(
    WorkflowTemplate(
        name="login_only",
        stages=[StageFactory.create_login_stage()],
        description="Simple login test"
    )
)

WorkflowTemplateRegistry.register_template(
    WorkflowTemplate(
        name="user_management",
        stages=[
            StageFactory.create_login_stage(),
            StageFactory.create_user_creation_stage(),
            StageFactory.create_cleanup_stage()
        ],
        description="User creation and cleanup without profile check"
    )
)