# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher

from pyvda import VirtualDesktop, get_virtual_desktops

class VirtualDesktopSwitcher(FlowLauncher):

    prev_vd_number:int = -1

    def query(self,  param: str = ''):

        results = []

        virtual_desktops = get_virtual_desktops()

        current_vd = VirtualDesktop(current=True)

        filter = param.strip().lower()
        
        for vd in virtual_desktops:
            name = ""
            try:
                name = vd.name
            except  NotImplementedError as e: pass

            if name == "":
                name = f"Desktop {vd.number}"

            if filter not in name.lower():
                continue

            score = 0
            subtitle = ""

            if vd.id == current_vd.id:
                # If this is the current vd, make sure its last using a low score
                score = -100

                subtitle = "Current Desktop"
            
            elif self.prev_vd_number == vd.number:
                # If this is the previous vd, prioritize it in the results
                score = 50

                subtitle = "Previous Desktop"

            results.append({
                "Title": name,
                "SubTitle": subtitle,
                "Score": score,
                "IcoPath": "assets/main_icon.png",
                "JsonRPCAction": {
                    "method": "switch_to_desktop",
                    "parameters": [vd.number]
                }
            })

        return results

    def switch_to_desktop(self, number:int):
        self.prev_vd_number = number

        VirtualDesktop(number).go()

if __name__ == "__main__":
    VirtualDesktopSwitcher()
