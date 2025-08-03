from rich import print as rprint
from testplan.testing.multitest import testcase, testsuite
from testplan.common.utils import helper

from thanos.stage import TestStage
from thanos.workflow import WorkflowRunner
from thanos.cache import TestCache
from thanos.stages.login import login_to_service
from thanos.stages.user import create_user, check_user_profile
from thanos.stages.cleanup import cleanup_data
from thanos.helpers import report_workflow_results


@testsuite
class PerformanceTestSuite(object):

    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.failures = []

    def setup(self, env, result):
        rprint(f"[bold cyan]Setting up Performance Test Suite: {self.name}[/bold cyan]")
        result.log(f"Setting up Performance Test Suite: {self.name}")
        # Here you can add any setup code if necessary
        self.test_cache = TestCache()
        self.runner = WorkflowRunner(cache=self.test_cache)

        # Save host environment variable in report.
        helper.log_environment(result)

        # Save host hardware information in report.
        helper.log_hardware(result)


    @testcase(
        name="WorkflowTest", 
        tags=["performance", "workflow"], 
        parameters={"rate": (2,4), "duration": (3,5), "threshold": (6, 20)},
    )
    def test_my_workflow(self, env, result, rate, duration, threshold):
        # Clear any existing stages from previous parameterized test runs
        self.runner.clear_stages()
        
        # Define the stages and their dependencies
        stage_login = TestStage(
            name="login_to_service",
            action=login_to_service,
            dependencies=[]
        )

        stage_create = TestStage(
            name="create_user",
            action=create_user,
            dependencies=["login_to_service"]
        )

        stage_check = TestStage(
            name="check_user_profile",
            action=check_user_profile,
            dependencies=["create_user"]
        )

        stage_cleanup = TestStage(
            name="cleanup_data",
            action=cleanup_data,
            dependencies=["create_user"] # Can be dependent on create_user to know which user to delete
        )

        # Add stages to the runner
        self.runner.add_stage(stage_login)
        self.runner.add_stage(stage_create)
        self.runner.add_stage(stage_check)
        self.runner.add_stage(stage_cleanup)

        # Run the tests and store the run_id
        run_id = self.runner.execute_workflow()

        # After the test run, the result is already in the cache.
        # We can now simulate uploading it to a database.
        # NOTE: moved this to teardown to ensure it runs after all tests
        ## self.runner.upload_to_db()
        
        # Generate enhanced final reporting
        report_workflow_results(self.runner)
        result.log(f"Test '{self.name}' executed with rate={rate}, duration={duration}, threshold={threshold}") 
        result.equal(self.runner.stages["check_user_profile"].status, "PASSED", description="Check user profile stage passed")
        result.equal(self.runner.stages["cleanup_data"].status, "PASSED", description="Cleanup stage passed")
        result.log("Workflow test completed successfully.")

        # You can also retrieve a specific run result from the cache
        retrieved_result = self.test_cache.get_run_result(run_id)
        if retrieved_result:
            rprint(f"\nRetrieved result for run '{retrieved_result.run_id}': Overall Status = {retrieved_result.overall_status}")
            # You could also iterate through retrieved_result.stage_results here
        else:
            rprint(f"\nNo results found for run ID: {run_id}")

    def teardown(self, env, result):
        result.log("Tearing down the test environment.")
        # Here you can add any cleanup code if necessary
        self.runner.upload_to_db()

        # Attach testplan.log file in report.
        helper.attach_log(result)