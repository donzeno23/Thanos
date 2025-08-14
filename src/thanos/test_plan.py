import sys
import os

from testplan import test_plan, Testplan
from testplan.testing.multitest import MultiTest
from testplan.report.testing.styles import Style, StyleEnum

from thanos.tests.test_suite_basic import BasicSuite
from thanos.tests.test_suite_performance import PerformanceTestSuite
from thanos.engine.eu.app_one.test_suite_one import PerfTestSuite


@test_plan(
    name='StageWorkflow Test Plan',
    # stdout_style=Style("testcase", "testcase")
    # stdout_style=Style(passing=StyleEnum.TESTCASE, failing=StyleEnum.ASSERTION)
    stdout_style=Style(passing="testcase", failing="assertion-detail"),
    pdf_path=os.path.join(os.path.dirname(__file__), "report.pdf"),
    pdf_style=Style(passing="testcase", failing="assertion-detail"),
)
def main(plan: Testplan):
    test = MultiTest(
       name='StageWorkflow Tests',
       suites=[BasicSuite(name='BasicSuite')]
    )
    performance_test = MultiTest(
       name='Performance Tests',
       suites=[PerformanceTestSuite(name='PerformanceTestSuite')]
    )

    perf_test_mt = MultiTest(
        name='PerfTestSuite',
        suites=[PerfTestSuite(name='PerfTestSuite')]
    )
    
    plan.add(test)
    plan.add(performance_test)
    plan.add(perf_test_mt)


if __name__ == '__main__':
  sys.exit(not main())
