"""
  Bring Back group.all_x (BBGAX)
  https://github.com/so3n/Bring-Back-group.all_x
"""

import appdaemon.plugins.hass.hassapi as hass

GROUPS = [
    dict(domain="automation", group_name="all_automations"),
    dict(domain="cover", group_name="all_covers"), 
    dict(domain="device_tracker", group_name="all_devices"), 
    dict(domain="fan", group_name="all_fans"), 
    dict(domain="light", group_name="all_lights"), 
    dict(domain="lock", group_name="all_locks"), 
    dict(domain="plant", group_name="all_plants"), 
    dict(domain="remote", group_name="all_remotes"), 
    dict(domain="script", group_name="all_scripts"), 
    dict(domain="switch", group_name="all_switches"), 
    dict(domain="vacuum", group_name="all_vacuum_cleaners"),
    dict(domain="person", group_name="all_people")
]

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
        grp_name = None
        
        for grp in GROUPS:
            if domain == grp["domain"]:
                grp_name = grp["group_name"] 
        
        if grp_name is None:
            self.log(f"{domain} not a valid domain! Skipping")
            return

        for dev in self.get_state(domain):
            entities.append(dev)
            
        self.log(f"Creating group.{grp_name} for {entities}")
        self.call_service("group/set", object_id=grp_name, entities=entities)
    
    def to_list(self, x):
        """ convert variable to list if not list """
        return x if type(x) is list else [x]
