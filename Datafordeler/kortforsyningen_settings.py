# -*- coding: utf-8 -*-
"""
/***************************************************************************
 KortforsyningenSettingsDialog
                                 A QGIS plugin
 Easy access to WMS from Kortforsyningen
                             -------------------
        begin                : 2015-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2015 Agency for Data supply and Efficiency
        email                : kortforsyningen@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from PyQt4 import QtGui, uic
from qgissettingmanager import SettingManager, SettingDialog

FORM_CLASS, _ = uic.loadUiType(
    os.path.join(os.path.dirname(__file__), 'kf_settings.ui')
)


class KFSettings(SettingManager):
    def __init__(self):
        SettingManager.__init__(self, 'Kortforsyningen')
        self.addSetting('username', 'string', 'global', '')
        self.addSetting('password', 'string', 'global', '')
        self.addSetting('remember_settings', 'bool', 'global', False)


class KFSettingsDialog(QtGui.QDialog, FORM_CLASS, SettingDialog):
    def __init__(self, settings):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        SettingDialog.__init__(self, settings)
