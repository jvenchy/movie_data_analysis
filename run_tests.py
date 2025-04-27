#!/usr/bin/env python3
"""
Test runner script to execute all tests
"""
import unittest
import sys
import os

# Add output directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import test modules
from test_analysis import TestAnalysisFunctions
from test_analysis_edge_cases import TestAnalysisEdgeCases
from test_pull_information import TestPullInformation
from test_pull_information_edge_cases import TestPullInformationEdgeCases

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestAnalysisFunctions))
    test_suite.addTest(unittest.makeSuite(TestAnalysisEdgeCases))
    test_suite.addTest(unittest.makeSuite(TestPullInformation))
    test_suite.addTest(unittest.makeSuite(TestPullInformationEdgeCases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate status code
    sys.exit(not result.wasSuccessful())
