#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from test.testapi import TestAPIMaker
import test.gui 
 
def suite():

    suite = unittest.TestSuite()
    
    all_test = [
    TestAPIMaker        
    ]
    for test in all_test :
        suite.addTest(unittest.makeSuite(test))   
    
    return suite

def main():
    test.gui.main()
    unittest.TextTestRunner(verbosity=2).run(suite())
    
if __name__ == "__main__":
    main()