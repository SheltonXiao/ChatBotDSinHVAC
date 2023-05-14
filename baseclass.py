# -*- coding:utf-8 -*-
'''
@File    :   app.py
@Time    :   2023/05/11 11:57:20
@Author  :   SheltonXiao
@Version :   1.0
@Contact :   pi620903@163.com
@Desc    :   None
@License :

    (c) Copyright 2022 SheltonXiao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or(at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY;without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License
    for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https: //www.gnu.org/licenses/>.
'''

# here put the import lib
import time

class Pool():
    def __init__(self, ):
        self.dict = {}
        self.update_time = {}
        # 1 hour
        self.time_interval = 60 * 60
    
    def __contains__(self, key):
        self._del_outdated()
        return key in self.dict
    
    def __getitem__(self, key):
        self._del_outdated()
        return self.dict[key]
    
    def __setitem__(self, key, value):
        self.dict[key] = value
        self.update_time[key] = time.time()
        self._del_outdated()
        
    def _del_outdated(self,):
        for key in self.update_time:
            if time.time() - self.update_time[key] > self.time_interval:
                del self.dict[key]
                del self.update_time[key]
        
    def __delitem__(self, key):
        del self.dict[key]


if __name__ == '__main__':
    pass
