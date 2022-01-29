@echo off
cls
:my_loop
IF %1=="" GOTO completed
  python c:\subscene_ar_select.py %1
  SHIFT
  GOTO my_loop
:completed