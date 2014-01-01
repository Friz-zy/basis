#!/usr/bin/env python
# coding=utf-8
"""
Copyright (c) by Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted 
provided that the following conditions are met:

a. Redistributions of source code must retain the above copyright notice, this list of 
conditions and the following disclaimer. 

b. Redistributions in binary form must reproduce the above copyright notice, this list of 
conditions and the following disclaimer in the documentation and/or other materials provided 
with the distribution. 

c. Neither the name of the nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
import os
import sys
import shutil
import six
from configobj import ConfigObj

class Config:
    def __init__(self, parent, name, defaultConfigPathPath=""):
        self.parent = parent
        self.name = str(name)
        self.homeDir = os.path.join(os.path.expanduser("~"), self.name)
        self.moduleDir = os.path.abspath(os.path.dirname(
                                sys.modules[self.__module__].__file__))
        
        self.homeConfigPath = os.path.join(self.homeDir, self.name + ".conf")
        if not defaultConfigPathPath:
            self.defaultConfigPath = os.path.join(self.moduleDir, self.name + ".conf")
        
        self.parent.homeDir = self.homeDir

    def createUserConfig(self, paths):
        if not os.path.isdir(self.homeDir):
            try:
                os.makedirs(self.homeDir)
            except:
                six.print_(("Error: can't create %s" % self.homeDir),
                                    file=sys.stderr, end="\n", sep=" ")
                six.print_(("Can not create user config"),
                           file=sys.stderr, end="\n", sep=" ")
                return 1

        for path in paths:
            if os.path.exists(os.path.join(self.homeDir, path)):
                continue
            if os.path.isdir(os.path.join(self.moduleDir, path)):
                try:
                    shutil.copytree(os.path.join(self.moduleDir, path),
                                        os.path.join(self.homeDir, path))
                except:
                    six.print_(("Error: can't create %s"  % os.path.join(self.homeDir, path)),
                                                            file=sys.stderr, end="\n", sep=" ")                                                                                                  
                    six.print_(("Maybe you haven't write acces to %s or %s doesn't exists" %  ((
                                                self.homeDir, os.path.join(self.moduleDir, path)))),
                                                                    file=sys.stderr, end="\n", sep=" ")

            elif os.path.exists(os.path.join(self.moduleDir, path)):
                try:
                    shutil.copy(os.path.join(self.moduleDir, path), os.path.join(self.homeDir, path))
                except:
                    six.print_(("Error: can't create %s"  % os.path.join(self.homeDir, path)),
                                                                file=sys.stderr, end="\n", sep=" ")                                                                                                  
                    six.print_(("Maybe you haven't write acces to %s or %s doesn't exists" %  ((
                                                self.homeDir, os.path.join(self.moduleDir, path)))),
                                                                    file=sys.stderr, end="\n", sep=" ")

        if os.path.isfile(self.defaultConfigPath) and not os.path.isfile(self.homeConfigPath):
            try:
                shutil.copy(self.defaultConfigPath, self.homeConfigPath)
            except:
                six.print_(("Error: can't create %s" % self.homeConfigPath),
                                            file=sys.stderr, end="\n", sep=" ")

    def loadConfig(self):
        try:
            config = ConfigObj(self.defaultConfigPath)
        except:
            six.print_(("Error: can't load %s as default config" % self.defaultConfigPath),
                                                        file=sys.stderr, end="\n", sep=" ")
            config = {}
        try:
            userConfig = ConfigObj(self.homeConfigPath)
        except:
            six.print_(("Error: can't load %s as user config" % self.homeConfigPath),
                                                    file=sys.stderr, end="\n", sep=" ")
            userConfig = {}
        
        self.config = dict(config.items() + userConfig.items())
        self.setFieldsFromDict(self.config)

    def setFieldsFromDict(self, d):
        for key in d.keys():
            if isinstance(d[key], dict):
                self.setFieldsFromDict(d[key])
            else:
                self.setField(key)

    def setField(self, field, default=None):
        if not field:
            six.print_(("can not set empty field to self"),
                            file=sys.stderr, end="\n", sep=" ")
            return 1
        elif self.config[field]:
            self.parent.__dict__[field] = self.config.get(field, default)

    def saveConfig(self, fields):
        try:
            userConfig = ConfigObj(self.homeConfigPath)
        except:
            six.print_(("Error: can't load %s as user config" % self.homeConfigPath),
                                                    file=sys.stderr, end="\n", sep=" ")
            userConfig = ConfigObj()
            for field in fields:
                userConfig[field] = self.parent.__dict__[field]

        for field in fields:
            self.setFieldToDict(field, userConfig)
        with open(self.homeConfigPath, "w") as file:
            userConfig.write(file)

    def setFieldToDict(self, field, d):
            for key in d.keys():
                if isinstance(d[key], dict):
                    self.setFieldToDict(field, d[key])
                elif  key == field:
                     d[key] = self.parent.__dict__[field]
                     
def loadConfig():
    # initialization of variables
    self.file = ""
    self.icons = ""
    self.images = ""
    
    '''
    set ~/name as home directory: self.homeDir
    set ~/name/name.conf as user config file
    set ./name.config as default config file
    '''
    self.config = Config(self, "name")
    
    '''
    create ~/name directory
    copy ./name.conf to ~/name/name.conf
    copy ./icons, ./images to ~/name/
    '''
    self.config.createUserConfig(["icons", "images"])
    
    '''
    load from config:
    self.file
    self.icons
    self.images
    '''
    self.config.loadConfig()

    # set default paths for icons and images directories
    if not self.icons:
        self.icons = os.path.join(self.homeDir, "icons")
        if not os.path.isdir(self.icons):
            self.icons = "./icons"

    if not self.images:
        self.images = os.path.join(self.homeDir, "images")
        if not os.path.isdir(self.images):
            self.images = "./images"

def saveConfig():
    '''
    save to ~/name/name.config variables:
    file
    icons
    images
    '''
    if not self.file:
        self.file = ""
    self.config.saveConfig(["file", "icons", "images"])