from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from rich import print as rprint
from testplan.testing.multitest import testcase, testsuite
from testplan.common.utils import helper

from thanos.stage import TestStage
from thanos.workflow import WorkflowRunner
from thanos.cache import TestCache
from thanos.helpers import report_workflow_results


@dataclass
class TestConfiguration:
    """Configuration for test parameters and behavior"""
    name: str
    tags: List[str]
    parameters: Dict[str, tuple]
    failure_conditions: Optional[Dict[str, Callable]] = None
    custom_assertions: Optional[Dict[str, Callable]] = None


@dataclass
class StageDefinition:
    """Definition for creating test stages"""
    name: str
    action: Callable
    dependencies: List[str]
    failure_condition: Optional[Callable] = None


class TestSuiteTemplate(ABC):
    """Abstract base class implementing Template Method pattern for test suites"""
    
    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.failures = []
        self.run_ids = []
        self.test_cache = None
        self.runner = None
    
    def setup(self, env, result):
        """Template method for setup - can be overridden for custom setup"""
        rprint(f"[bold cyan]Setting up Test Suite: {self.name}[/bold cyan]")
        result.log(f"Setting up Test Suite: {self.name}")
        
        self.test_cache = TestCache()
        self.runner = WorkflowRunner(cache=self.test_cache)
        
        # Common setup operations
        helper.log_environment(result)
        helper.log_hardware(result)
        
        # Allow subclasses to add custom setup
        self.custom_setup(env, result)
    
    def teardown(self, env, result):
        """Template method for teardown - can be overridden for custom teardown"""
        result.log("Tearing down the test environment.")
        
        # Allow subclasses to add custom teardown
        self.custom_teardown(env, result)
        
        # Common teardown operations
        self.runner.upload_to_db()
        helper.attach_log(result)
    
    def execute_workflow_test(self, env, result, **test_params):
        """Template method for workflow execution"""
        self.runner.clear_stages()
        
        # Get stage definitions from subclass
        stage_definitions = self.get_stage_definitions()
        
        # Build and add stages
        stages = self._build_stages(stage_definitions, test_params)
        for stage in stages:
            self.runner.add_stage(stage)
        
        # Apply failure conditions if any
        self._apply_failure_conditions(stages, test_params)
        
        # Execute workflow
        run_id = self.runner.execute_workflow()
        
        # Generate reporting
        report_workflow_results(self.runner)
        result.log(f"Test '{self.name}' executed with parameters: {test_params}")
        
        # Perform assertions
        self._perform_assertions(result, test_params)
        
        # Handle cache results
        self._handle_cache_results(run_id)
        
        return run_id
    
    @abstractmethod
    def get_stage_definitions(self) -> List[StageDefinition]:
        """Abstract method - subclasses must define their stages"""
        pass
    
    @abstractmethod
    def get_test_configuration(self) -> TestConfiguration:
        """Abstract method - subclasses must define their test configuration"""
        pass
    
    def custom_setup(self, env, result):
        """Hook for custom setup - override if needed"""
        pass
    
    def custom_teardown(self, env, result):
        """Hook for custom teardown - override if needed"""
        pass
    
    def _build_stages(self, stage_definitions: List[StageDefinition], test_params: Dict) -> List[TestStage]:
        """Build TestStage objects from definitions"""
        stages = []
        for stage_def in stage_definitions:
            stage = TestStage(
                name=stage_def.name,
                action=stage_def.action,
                dependencies=stage_def.dependencies
            )
            stages.append(stage)
        return stages
    
    def _apply_failure_conditions(self, stages: List[TestStage], test_params: Dict):
        """Apply failure conditions based on test parameters"""
        stage_definitions = self.get_stage_definitions()
        
        for stage, stage_def in zip(stages, stage_definitions):
            if stage_def.failure_condition and stage_def.failure_condition(test_params):
                # Create failure action
                original_action = stage.action
                def failing_action(context):
                    rprint(f"[red]👤 Simulating failure in {stage.name}[/red]")
                    raise Exception(f"Simulated failure for {stage.name}")
                stage.action = failing_action
    
    def _perform_assertions(self, result, test_params: Dict):
        """Perform test assertions based on configuration"""
        config = self.get_test_configuration()
        
        # Default assertions
        self._default_assertions(result, test_params)
        
        # Custom assertions if defined
        if config.custom_assertions:
            for assertion_name, assertion_func in config.custom_assertions.items():
                assertion_func(result, self.runner, test_params)
    
    def _default_assertions(self, result, test_params: Dict):
        """Default assertion logic - can be overridden"""
        # Check if any failure conditions were met
        stage_definitions = self.get_stage_definitions()
        expected_failures = any(
            stage_def.failure_condition and stage_def.failure_condition(test_params)
            for stage_def in stage_definitions
        )
        
        if expected_failures:
            # Find the first stage that should fail
            for stage_def in stage_definitions:
                if stage_def.failure_condition and stage_def.failure_condition(test_params):
                    result.fail(f"Expected failure for {stage_def.name}")
                    result.equal(
                        self.runner.stages[stage_def.name].status, 
                        "FAILED", 
                        description=f"{stage_def.name} should fail"
                    )
                    break
        else:
            # All stages should pass
            for stage_name, stage in self.runner.stages.items():
                if stage.status not in ["SKIPPED"]:
                    result.equal(
                        stage.status, 
                        "PASSED", 
                        description=f"{stage_name} should pass"
                    )
            result.log("Workflow test completed successfully.")
    
    def _handle_cache_results(self, run_id: str):
        """Handle cached results display"""
        retrieved_result = self.test_cache.get_run_result(run_id)
        if retrieved_result:
            rprint(f"\nRetrieved result for run '{retrieved_result.run_id}': Overall Status = {retrieved_result.overall_status}")
        else:
            rprint(f"\nNo results found for run ID: {run_id}")


def create_test_suite_class(base_class: type, config: TestConfiguration):
    """Factory function to create test suite classes dynamically"""
    
    @testsuite
    class DynamicTestSuite(base_class):
        def __init__(self, name: str):
            super().__init__(name)
        
        @testcase(
            name=config.name,
            tags=config.tags,
            parameters=config.parameters
        )
        def test_workflow(self, env, result, **test_params):
            return self.execute_workflow_test(env, result, **test_params)
    
    return DynamicTestSuite