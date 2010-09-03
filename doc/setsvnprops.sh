#!/bin/sh

svn -R propset svn:ignore -F .svnignore .
svn -R propset svn:keywords -F .svnkeywords *
svn -R propset svn:keywords -F .svnkeywords */*
svn -R propset svn:keywords -F .svnkeywords */*/*
