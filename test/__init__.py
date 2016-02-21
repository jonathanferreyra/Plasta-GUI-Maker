#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test.test_add_maker import TestAddMaker

def suite():

    suite = unittest.TestSuite()

    all_test = [
        TestAddMaker
    ]
    for test in all_test :
        suite.addTest(unittest.makeSuite(test))

    return suite

def main():
    unittest.TextTestRunner(verbosity=2).run(suite())

if __name__ == "__main__":
    main()