from typing import List
from testplan.testing.multitest import testcase, testsuite

from thanos.testing.base_test_suite import TestSuiteTemplate, TestConfiguration, StageDefinition
from thanos.testing.stage_factory import StageFactory
from thanos.testing.test_builder import create_performance_test_config


@testsuite
class PerfTestSuite(TestSuiteTemplate):
    """Performance test suite using the new template-based architecture"""
    
    def get_stage_definitions(self) -> List[StageDefinition]:
        """Define the workflow stages using the factory"""
        return StageFactory.create_standard_workflow()
    
    def get_test_configuration(self) -> TestConfiguration:
        """Define test configuration using the builder"""
        return create_performance_test_config().build()
    
    @testcase(
        name="WorkflowTest", 
        tags=["performance", "workflow"], 
        parameters={"rate": (2,4), "duration": (3,5), "threshold": (6, 20)},
    )
    def test_my_workflow(self, env, result, rate, duration, threshold):
        """Execute workflow test using template method"""
        return self.execute_workflow_test(env, result, rate=rate, duration=duration, threshold=threshold)