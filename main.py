# -*- coding: utf-8 -*-

import sys,os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from pyflowlauncher import Plugin, Result, api

from pyvda import VirtualDesktop, get_virtual_desktops

plugin = Plugin()

previous_desktop_id = None


@plugin.on_method
def switch_desktop(desktop_id: str):
    global previous_desktop_id

    desktop = next(
        (vd for vd in get_virtual_desktops() if str(vd.id) == desktop_id),
        None
    )
    if desktop is None:
        return

    previous_desktop_id = VirtualDesktop.current().id
    desktop.go()

    return api.change_query(plugin.manifest.action_keyword + " ", requery=True)


@plugin.on_method
def query(query:str):

    results:list[Result] = []

    virtual_desktops = get_virtual_desktops()

    current_vd = VirtualDesktop(current=True)
    filter = query.strip().lower()
    
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
        
        # prioritize desktops of which any word in its name has the filter as a prefix, ie exact match as you type
        if any(map(
            lambda w: w.startswith(filter), 
            name.lower().split(" ")
        )):
            score += 500

        results.append(
            Result(
                title=name,
                subtitle=subtitle,
                icon="assets/main_icon.png",
                score=score
            ).add_action(
                switch_desktop, 
                [str(vd.id)]
            )
        )

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
