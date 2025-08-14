from typing import Dict, List, Callable, Optional, Any
from dataclasses import dataclass, field

from .base_test_suite import TestConfiguration, StageDefinition
from .stage_factory import WorkflowTemplateRegistry


class TestConfigurationBuilder:
    """Builder pattern for creating test configurations"""
    
    def __init__(self):
        self._name: str = "DefaultTest"
        self._tags: List[str] = ["workflow"]
        self._parameters: Dict[str, tuple] = {"rate": (2, 4), "duration": (3, 5), "threshold": (6, 20)}
        self._failure_conditions: Optional[Dict[str, Callable]] = None
        self._custom_assertions: Optional[Dict[str, Callable]] = None
    
    def with_name(self, name: str) -> 'TestConfigurationBuilder':
        """Set test name"""
        self._name = name
        return self
    
    def with_tags(self, tags: List[str]) -> 'TestConfigurationBuilder':
        """Set test tags"""
        self._tags = tags
        return self
    
    def with_parameters(self, parameters: Dict[str, tuple]) -> 'TestConfigurationBuilder':
        """Set test parameters"""
        self._parameters = parameters
        return self
    
    def with_failure_conditions(self, conditions: Dict[str, Callable]) -> 'TestConfigurationBuilder':
        """Set failure conditions"""
        self._failure_conditions = conditions
        return self
    
    def with_custom_assertions(self, assertions: Dict[str, Callable]) -> 'TestConfigurationBuilder':
        """Set custom assertions"""
        self._custom_assertions = assertions
        return self
    
    def add_parameter(self, name: str, values: tuple) -> 'TestConfigurationBuilder':
        """Add a single parameter"""
        self._parameters[name] = values
        return self
    
    def add_tag(self, tag: str) -> 'TestConfigurationBuilder':
        """Add a single tag"""
        if tag not in self._tags:
            self._tags.append(tag)
        return self
    
    def build(self) -> TestConfiguration:
        """Build the test configuration"""
        return TestConfiguration(
            name=self._name,
            tags=self._tags,
            parameters=self._parameters,
            failure_conditions=self._failure_conditions,
            custom_assertions=self._custom_assertions
        )


class TestSuiteBuilder:
    """Builder for creating complete test suite implementations"""
    
    def __init__(self):
        self._workflow_template: str = "standard_user_workflow"
        self._config_builder: TestConfigurationBuilder = TestConfigurationBuilder()
        self._custom_stages: List[StageDefinition] = []
        self._suite_name: str = "TestSuite"
    
    def with_workflow_template(self, template_name: str) -> 'TestSuiteBuilder':
        """Use a predefined workflow template"""
        self._workflow_template = template_name
        return self
    
    def with_suite_name(self, name: str) -> 'TestSuiteBuilder':
        """Set the test suite class name"""
        self._suite_name = name
        return self
    
    def with_test_config(self, config_builder: TestConfigurationBuilder) -> 'TestSuiteBuilder':
        """Set the test configuration builder"""
        self._config_builder = config_builder
        return self
    
    def add_custom_stage(self, stage: StageDefinition) -> 'TestSuiteBuilder':
        """Add a custom stage to the workflow"""
        self._custom_stages.append(stage)
        return self
    
    def build_concrete_suite(self, base_template_class):
        """Build a concrete test suite class"""
        from .base_test_suite import TestSuiteTemplate
        
        # Get workflow template
        workflow_template = WorkflowTemplateRegistry.get_template(self._workflow_template)
        stages = workflow_template.stages + self._custom_stages
        
        # Build configuration
        config = self._config_builder.build()
        
        class ConcreteTestSuite(base_template_class):
            def __init__(self, name: str):
                super().__init__(name)
            
            def get_stage_definitions(self) -> List[StageDefinition]:
                return stages
            
            def get_test_configuration(self) -> TestConfiguration:
                return config
        
        # Set the class name dynamically
        ConcreteTestSuite.__name__ = self._suite_name
        ConcreteTestSuite.__qualname__ = self._suite_name
        
        return ConcreteTestSuite


# Convenience functions for common configurations
def create_performance_test_config() -> TestConfigurationBuilder:
    """Create a standard performance test configuration"""
    return (TestConfigurationBuilder()
            .with_name("WorkflowTest")
            .with_tags(["performance", "workflow"])
            .with_parameters({"rate": (2, 4), "duration": (3, 5), "threshold": (6, 20)}))


def create_smoke_test_config() -> TestConfigurationBuilder:
    """Create a smoke test configuration"""
    return (TestConfigurationBuilder()
            .with_name("SmokeTest")
            .with_tags(["smoke", "basic"])
            .with_parameters({"rate": (1,), "duration": (1,)}))


def create_load_test_config() -> TestConfigurationBuilder:
    """Create a load test configuration"""
    return (TestConfigurationBuilder()
            .with_name("LoadTest")
            .with_tags(["load", "performance"])
            .with_parameters({"rate": (10, 20, 50), "duration": (30, 60), "concurrent_users": (5, 10)}))