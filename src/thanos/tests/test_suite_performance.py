from rich import print as rprint
from testplan.testing.multitest import testcase, testsuite

from thanos.stage import TestStage
from thanos.workflow import WorkflowRunner
from thanos.stages.login import login_to_service
from thanos.stages.user import create_user, check_user_profile
from thanos.stages.cleanup import cleanup_data


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

    @testcase(
        name="WorkflowTest", 
        tags=["performance", "workflow"], 
        parameters={"rate": (2,4), "duration": (3,5), "threshold": (6, 20)},
    )
    def test_my_workflow(self, env, result, rate, duration, threshold):
        # TODO: should the WorkflowRunner be initialized here, in setup or in the main test plan?
        runner = WorkflowRunner()

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
        runner.add_stage(stage_login)
        runner.add_stage(stage_create)
        runner.add_stage(stage_check)
        runner.add_stage(stage_cleanup)

        # Run the tests
        runner.execute_workflow()
        
        # Enhanced final reporting
        rprint("\n[bold cyan]📊 === FINAL RESULTS ===[/bold cyan]")
        rprint(f"[bold green]🎆 Test run completed successfully![/bold green]")
        
        rprint("\n[bold yellow]📝 Final context:[/bold yellow]")
        rprint(f"[dim]{runner.context}[/dim]")
        
        rprint("\n[bold magenta]📈 Stage results:[/bold magenta]")
        for stage_name, stage in runner.stages.items():
            status_icon = "✅" if stage.status == "PASSED" else "❌" if stage.status == "FAILED" else "⏭️"
            status_color = "green" if stage.status == "PASSED" else "red" if stage.status == "FAILED" else "yellow"
            rprint(f"  {status_icon} [cyan]{stage_name}[/cyan]: [{status_color}]{stage.status}[/{status_color}] [dim](Result: {stage.result})[/dim]")
        
        rprint("\n[bold cyan]========================[/bold cyan]\n")
        result.log(f"Test '{self.name}' executed with rate={rate}, duration={duration}, threshold={threshold}") 
        result.equal(runner.stages["check_user_profile"].status, "PASSED", description="Check user profile stage passed")
        result.equal(runner.stages["cleanup_data"].status, "PASSED", description="Cleanup stage passed")
        result.log("Workflow test completed successfully.")

    def teardown(self, env, result):
        result.log("Tearing down the test environment.")
        # Here you can add any cleanup code if necessary