from vindula.services.testing import FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest2 as unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("robot_test.txt"),
                layer=FUNCTIONAL_TESTING)
    ])
    return suite
