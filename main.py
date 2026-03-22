# -*- coding: utf-8 -*-

import functools
import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flogin import ExecuteResponse, Plugin, Query, Result

from pyvda import VirtualDesktop, get_virtual_desktops

plugin = Plugin()

class DesktopResult(Result):
    def __init__(self, desktop_number:int, title: str, subtitle:str) -> None:
        super().__init__(title, sub=subtitle, icon="assets/main_icon.png")

        self.desktop_number = desktop_number

    async def callback(self):
        switch_to_desktop(self.desktop_number)

        return ExecuteResponse(True)

@plugin.search()
async def query(query:Query):

    results:list[DesktopResult] = []

    virtual_desktops = get_virtual_desktops()

    current_vd = VirtualDesktop(current=True)
    filter = query.text.strip().lower()
    
    for vd in virtual_desktops:
        name = get_desktop_name(vd)

        if filter not in name.lower():
            continue

        score = 0
        subtitle = ""

        if vd.id == current_vd.id:
            # If this is the current vd, make sure its last using a low score
            score = -100

            subtitle = "Current Desktop"
    

        results.append(DesktopResult(
            desktop_number=vd.number,
            title=name,
            subtitle=subtitle,
        ))

    return results
    
def get_desktop_name(vd:VirtualDesktop):
    name = ""
    try:
        name = vd.name
    except  NotImplementedError as e: pass

    if name == "":
        name = f"Desktop {vd.number}"
    
    return name

def switch_to_desktop(number:int):
    VirtualDesktop(number).go()

plugin.run()
