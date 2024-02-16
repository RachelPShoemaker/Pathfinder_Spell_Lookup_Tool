class Spell:
    def __init__(self):
        self.name = " "
        self.actions = " "
        self.traits = []
        self.school = " "
        self.traditions = []
        self.cast = []
        self.deities = []
        self.requirement = " "
        self.trigger = " "
        self.cost = " "
        self.range = " "
        self.target = " "
        self.area = " "
        self.duration = " "
        self.save_throw = " "
        self.description = " "
    
    def print_spell(self):
        print('Spell name: ',self.name)
        print(self.actions)
        if(self.school != " "): print('School: ',self.school)
        if(self.traits != []): print('Traits:',', '.join(self.traits))
        if(self.traditions != []): print('Tradition(s): ',', '.join(self.traditions))
        if(self.cast != []): print('Cast type:',', '.join(self.cast))
        if(self.deities != []): print('Deities:',', '.join(self.deities))
        if(self.requirement != ""): print('Requirements:',self.requirement)
        if(self.trigger != ""): print('Trigger:',self.trigger)
        if(self.cost != ""): print('Cost:',self.cost)
        if(self.range != ""): print('Range:',self.range)
        if(self.target != ""): print('Target:',self.target)
        if(self.area != ""): print('Area:',self.area)
        if(self.duration != ""): print('Duration:',self.duration)
        if(self.save_throw != ""): print('Saving throw:',self.save_throw)
        print('\n',self.description)
        print("------------------------------------")
    
    def listToString(self, my_list):
        return ', '.join(my_list)
    
    def toTable(self):
        spellTable = [
            ['Name', 'Traits'],
            [self.name, self.listToString(self.traits)],
            ['Magic Tradition', 'School', 'Cast'],
            [self.listToString(self.traditions), self.school, self.listToString(self.cast)],
            ['Requirement', 'Range', 'Target'],
            [self.requirement, self.range, self.target],
            ['Area', 'Duration', 'Saving throw'],
            [self.area, self.duration, self.save_throw]
            # ['Description'],
            # [self.description]
        ]
        return spellTable
