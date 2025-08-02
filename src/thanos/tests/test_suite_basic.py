from rich import print as rprint

from testplan.testing.multitest import testcase, testsuite


def multiply(numA, numB):
    return numA * numB


@testsuite
class BasicSuite(object):

    def __init__(self, name: str):
        self.name = name
        self.tests = []
        self.failures = []

    def setup(self, env, result):
        """Setup method to initialize the test environment."""
        rprint(f"Setting up {self.name}...")
        result.log(f"Setting up {self.name}...")

    @testcase(
        name="BasicMultiplyTest", 
        tags=["math", "basic"], 
        parameters={"numA": (2,4), "numB": (3,5), "product": (6, 20)},
    )
    def basic_multiply(self, env, result, numA, numB, product):
        result.equal(multiply(numA, numB), product, description='Passing assertion')

    def teardown(self, env, result):
        result.log("Tearing down the test environment.")
        # Here you can add any cleanup code if necessary