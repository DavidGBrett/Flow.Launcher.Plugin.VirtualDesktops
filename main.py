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
            name = self.get_desktop_name(vd)

            if filter not in name.lower():
                continue

            score = 0
            subtitle = ""

            if vd.id == current_vd.id:
                # If this is the current vd, make sure its last using a low score
                score = -100

                subtitle = "Current Desktop"
        

            results.append({
                "Title": name,
                "SubTitle": subtitle,
                "Score": score,
                "IcoPath": "assets/main_icon.png",
                "ContextData":vd.number,
                "JsonRPCAction": {
                    "method": "switch_to_desktop",
                    "parameters": [vd.number]
                }
            })

        return results
    
    def context_menu(self, data):
        results = []

        match data:
            case int() as vd_number:
                                
                results.append({
                    "Title": "Delete",
                    "SubTitle": f"Delete this virtual desktop",
                    "JsonRPCAction": {
                        "method": "delete_desktop",
                        "parameters": [vd_number]
                    }
                })


        return results
    
    def get_desktop_name(self, vd:VirtualDesktop):
        name = ""
        try:
            name = vd.name
        except  NotImplementedError as e: pass

        if name == "":
            name = f"Desktop {vd.number}"
        
        return name

    def switch_to_desktop(self, number:int):

        VirtualDesktop(number).go()

    def delete_desktop(self, number:int):
        VirtualDesktop(number=number).remove()

if __name__ == "__main__":
    VirtualDesktopSwitcher()
