TARGETS := ../ui_mainwindow.py ../ui_newdialog.py

all: $(TARGETS)

../ui_mainwindow.py: mainwindow.ui
	pyuic4 mainwindow.ui > ../ui_mainwindow.py
../ui_newdialog.py: newdialog.ui
	pyuic4 newdialog.ui > ../ui_newdialog.py
