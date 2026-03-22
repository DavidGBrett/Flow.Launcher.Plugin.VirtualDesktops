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
    def __init__(self, desktop:VirtualDesktop, title: str, subtitle:str) -> None:
        super().__init__(title, sub=subtitle, icon="assets/main_icon.png")

        self.desktop = desktop

    async def callback(self):
        # switch to given virtual desktop
        self.desktop.go()

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
            desktop=vd,
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

plugin.run()
