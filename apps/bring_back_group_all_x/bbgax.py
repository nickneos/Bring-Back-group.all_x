"""
  Bring Back group.all_x (BBGAX)
  https://github.com/so3n/Bring-Back-group.all_x
"""

import appdaemon.plugins.hass.hassapi as hass

GROUP_DICT = {
    "automation": "all_automations",
    "cover": "all_covers", 
    "device_tracker": "all_devices", 
    "fan": "all_fans", 
    "light": "all_lights", 
    "lock": "all_locks", 
    "plant": "all_plants", 
    "remote": "all_remotes", 
    "script": "all_scripts", 
    "switch": "all_switches", 
    "vacuum": "all_vacuum_cleaners",
    "calendar": "all_calendar", 
    "remember_the_milk_account": "all_remember_the_milk_accounts", 
    "person": "all_people"
}


class group_all_x(hass.Hass):
    """ Create Default Groups """

    def initialize(self):
        """ initialize app """
        domains = self.to_list(self.args.get("domains", []))

        for domain in domains:
            self.create_group(domain)


    def create_group(self, domain):
        """ create group from supplied domain """
        entities = []
        grp_name = GROUP_DICT.get(domain, None)
        
        if grp_name is None:
            self.log(f"{domain} not a valid domain! Skipping")
            return

        for dev in self.get_state(domain):
            entities.append(dev)
        
        if not entities:
            self.log(f"No entities found for {domain}! Skipping")
            return
            
        self.log(f"Creating group.{grp_name} for {entities}")
        self.call_service("group/set", object_id=grp_name, entities=entities)
    
    
    def to_list(self, x):
        """ convert variable to list if not list """
        return x if type(x) is list else [x]
