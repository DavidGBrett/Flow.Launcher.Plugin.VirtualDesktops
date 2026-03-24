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

previous_desktop_id = None

class DesktopResult(Result):
    def __init__(self, desktop:VirtualDesktop, title: str, subtitle:str, score:int|None) -> None:
        super().__init__(title, sub=subtitle, icon="assets/main_icon.png",score=score)

        self.desktop = desktop

    async def callback(self):
        # update previous desktop id
        global previous_desktop_id
        previous_desktop_id = VirtualDesktop.current().id
        
        # switch to given virtual desktop
        self.desktop.go()

        await plugin.api.change_query(plugin.metadata.main_keyword+" ",requery=True)

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

        # Show the current desktop last since you are unlikely to want to change to it
        if vd.id == current_vd.id:
            score = -1000 # show lower in the list with low score
            subtitle = "Current Desktop"

        # show previous desktop first, so you can easily switch back
        elif vd.id == previous_desktop_id:
            score = 1000 # trying to show it as high as possible
            subtitle = "Previous Desktop"

        results.append(DesktopResult(
            desktop=vd,
            title=name,
            subtitle=subtitle,
            score=score
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
