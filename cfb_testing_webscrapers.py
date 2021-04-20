#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 19:46:09 2021

@author: sarahrodgers

Testing Web Scraper Results
"""

import unittest
from cfb_dictionaries import *
from cfb_dataframe import *

# testing that the web scraped information was pulled correctly from Wikipedia
class CFBWikipediaTestCase(unittest.TestCase): #must inherit from unittest.TestCase

    # Are all school names stored correctly as keys
    def test_1(self):
        self.assertEqual(len(nicknames.keys()), 131)
    
    # Are all mascot names stored correctly as values
    def test_2(self):
        self.assertEqual(len(nicknames.values()), 131)
        
    # Is the expected mascot associated with the correct school
    def test_3(self):
        self.assertEqual(nicknames["Penn State"], 'Nittany Lions')
        
    def test_4(self):
        self.assertEqual(nicknames["Virginia"], 'Cavaliers')
        
    def test_5(self):
        self.assertEqual(nicknames.get('Air Force'), 'Falcons')
        
    def test_6(self):
        self.assertEqual(nicknames.get('Syracuse'), 'Orange')
        
    # Check that there are no missing mascot values for schools with known mascots
    def test_7(self):
        self.assertFalse(nicknames['Ohio State'] == '', msg= "The Ohio State mascot is not missing")
    
    def test_8(self):
        self.assertFalse(nicknames['Michigan'] == '', msg= "The Michigan mascot is not missing")
   
# testing that the web scraped information was pulled correctly from ESPN
class CFBESPNTestCase(unittest.TestCase): #must inherit from unittest.TestCase
    
    # Are all school names stored correctly as keys
    def test_9(self):
        self.assertEqual(len(logos.keys()),  131)
    
    # Are all logos stored correctly as values
    def test_10(self):
        self.assertEqual(len(logos.values()),  131)
        
    # Is the expected logo id associated with the correct school
    def test_11(self):
        self.assertTrue('50' in logos['Penn State'])
        
    def test_12(self):
        self.assertTrue('333' in logos['Alabama'])
        
    # Check that there are no missing logo values for schools with known logos
    def test_13(self):
        self.assertFalse(logos['Auburn'] == '', msg= "The Auburn logo is not missing")
    
    def test_14(self):
        self.assertFalse(logos['Navy'] == '', msg= "The Navy logo is not missing")

if __name__ == '__main__':
    log_file = 'CFB Testing.txt'
    with open(log_file, "w") as f:
        runner = unittest.TextTestRunner(f)
        unittest.main(testRunner=runner)