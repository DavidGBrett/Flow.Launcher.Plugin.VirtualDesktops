# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

from pyvda import VirtualDesktop, get_virtual_desktops

class VirtualDesktopSwitcher(FlowLauncher):

    def query(self,  param: str = ''):

        results = []

        virtual_desktops = get_virtual_desktops()

        current_vd = VirtualDesktop(current=True)

        filter = param.strip().lower()
        
        for vd in virtual_desktops:
            is_current:bool = vd == current_vd

            if is_current: continue

            if filter not in vd.name.lower():
                continue

            results.append({
                "Title": vd.name,
                "SubTitle": "",
                "IcoPath": "assets/main_icon.png",
                "JsonRPCAction": {
                    "method": "switch_to_desktop",
                    "parameters": [vd.number]
                }
            })

        return results

    def switch_to_desktop(self, number:int):
        VirtualDesktop(number).go()

if __name__ == "__main__":
    VirtualDesktopSwitcher()
