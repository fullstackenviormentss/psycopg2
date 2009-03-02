#!/usr/bin/env python
# extras_dictcursor - test if DictCursor extension class works
#
# Copyright (C) 2004 Federico Di Gregorio  <fog@debian.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import psycopg2
import psycopg2.extras
import unittest

import tests


class ExtrasDictCursorTests(unittest.TestCase):
    """Test if DictCursor extension class works."""

    def setUp(self):
        self.conn = psycopg2.connect(tests.dsn)
        curs = self.conn.cursor()
        curs.execute("CREATE TEMPORARY TABLE ExtrasDictCursorTests (foo text)")
        curs.execute("INSERT INTO ExtrasDictCursorTests VALUES ('bar')")
        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def testDictCursorWithPlainCursorFetchOne(self):
        self._testWithPlainCursor(lambda curs: curs.fetchone())

    def testDictCursorWithPlainCursorFetchMany(self):
        self._testWithPlainCursor(lambda curs: curs.fetchmany(100)[0])

    def testDictCursorWithPlainCursorFetchAll(self):
        self._testWithPlainCursor(lambda curs: curs.fetchall()[0])

    def testDictCursorWithPlainCursorIter(self):
        def getter(curs):
            for row in curs:
                return row
        self._testWithPlainCursor(getter)
        
    def testDictCursorWithNamedCursorFetchOne(self):
        self._testWithNamedCursor(lambda curs: curs.fetchone())

    def testDictCursorWithNamedCursorFetchMany(self):
        self._testWithNamedCursor(lambda curs: curs.fetchmany(100)[0])

    def testDictCursorWithNamedCursorFetchAll(self):
        self._testWithNamedCursor(lambda curs: curs.fetchall()[0])

    def testDictCursorWithNamedCursorIter(self):
        def getter(curs):
            for row in curs:
                return row
        self._testWithNamedCursor(getter)

    def _testWithPlainCursor(self, getter):
        curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        curs.execute("SELECT * FROM ExtrasDictCursorTests")
        row = getter(curs)
        self.failUnless(row['foo'] == 'bar')
        self.failUnless(row[0] == 'bar')

    def _testWithNamedCursor(self, getter):
        curs = self.conn.cursor('aname', cursor_factory=psycopg2.extras.DictCursor)
        curs.execute("SELECT * FROM ExtrasDictCursorTests")
        row = getter(curs)
        self.failUnless(row['foo'] == 'bar')
        self.failUnless(row[0] == 'bar')

def test_suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == "__main__":
    unittest.main()
