from googlesearch import search
from bs4 import BeautifulSoup
import requests
from spell import Spell

def clean_action_text(text):
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('  ', ' ')
    text = text.replace('-', ' ')
    return text

def clean_spaces(text):
    return "WIP"

def scrape_actions(soup):
    VALID_TEXT = [" ", "[reaction]", "[one-action]", "[two-actions]", "[three-actions]", "  to  ", "  or  ", "  to 2 rounds"]
    dom_element = soup.find(string="Cast")
    dom_element = dom_element.next
    dom_str = dom_element.get_text() # Stores the dom text. It updates after each iteration.
    action_text = "" # Each valid dom iteration is appended to this.
    prev_text = "" # This variable is used to prevent duplicate text.
    while(dom_str in VALID_TEXT or dom_str == ""):
        if(dom_str != " " and dom_str != prev_text): 
            action_text += dom_str
            prev_text = dom_str
        dom_element = dom_element.next
        dom_str = dom_element.get_text()
    if(action_text == ""): # if action_text is empty, that means this spell has a cast time instead of actions.
        cast = soup.find(string="Cast")
        cast = cast.next.get_text()
        cast = cast[1:-2] # Cuts off unnecessary text. The first char is ' ' and the Last two chars are ' ' and '(' 
        return "Cast Time:" + cast
    action_text = clean_action_text(action_text)
    return action_text 

def scrape_traits(soup):
    SCHOOLS = ["Abjuration","Conjuration","Divination","Enchantment","Evocation","Illusion","Necromancy","Transmutation"]
    trait_list = ["",[]] # The first element is the school string, second element is a list of traits.
    if(soup.find(class_='traituncommon') is not None): trait_list[1].append("Uncommon") # DOM stores Uncommon and Rare in a different spot than other traits
    if(soup.find(class_='traitrare') is not None): trait_list[1].append("Rare")
    traits = soup.find_all(class_='trait')
    for trait in traits:
        if(trait.get_text() in SCHOOLS): trait_list[0] = trait.get_text()
        else: trait_list[1].append(trait.get_text())
    return trait_list

def scrape_traditions(soup):
    # The best way to find the traditions is to search the number of links to each type of tradition.
    # All spell webpages have at least one link to each tradition. So, we need to see if a particular spell has 2 or more links to a tradition. 
    tradition_list = []
    all_arcane_links = soup.find_all(href='SpellLists.aspx?Tradition=1')
    if(len(all_arcane_links) > 1): tradition_list.append("Arcane")
    all_divine_links = soup.find_all(href='SpellLists.aspx?Tradition=2')
    if(len(all_divine_links) > 1): tradition_list.append("Divine")
    all_occult_links = soup.find_all(href='SpellLists.aspx?Tradition=3')
    if(len(all_occult_links) > 1): tradition_list.append("Occult")
    all_primal_links = soup.find_all(href='SpellLists.aspx?Tradition=4')
    if(len(all_primal_links) > 1): tradition_list.append("Primal")
    return tradition_list

def scrape_deities(soup):
    deities_element = soup.find(string="Deities")
    deities_list = []
    prev_deities = ""
    if(deities_element is not None):
        while(deities_element.next.name != 'br'):
            deities_element = deities_element.next
            deities_str = deities_element.get_text()
            if(deities_str != "" and prev_deities != deities_str): 
                deities_list.append(deities_str)
                prev_deities = deities_str
    return deities_list
    
def scrape_cast_type(soup):
    cast_type = []
    if(soup.find(href='Rules.aspx?ID=283') is not None): cast_type.append("Somatic")
    if(soup.find(href='Rules.aspx?ID=284') is not None): cast_type.append("Verbal")
    if(soup.find(href='Rules.aspx?ID=282') is not None): cast_type.append("Material")
    return cast_type

def scrape_description(soup):
    # TODO: Fix bug. Unordered lists are printed 3 times instead of once.
    hr_tags = soup.find_all('hr') 
    description_element = hr_tags[2] # Stores DOM element. The spell description text starts after the 3rd hr break on the website.
    description_str = description_element.get_text()  # Value updates after each iteration.
    description_text = description_str # Stores the entire description text. Each valid "description_str" update will be appended to this. 
    prev_description = description_str # This will be used to prevent duplicate text. NOTE: Doesn't work for unordered lists.
    # This while-loop lets the program scrape the rest of the text I need.
    while(description_element.next.name != 'div'):
        description_element = description_element.next
        if(description_element.name == 'br' or description_element.name == 'hr'):
            description_text += '\n'
        description_str = description_element.get_text()  
        if(description_str != "" and prev_description != description_str): 
            description_text += description_str
            prev_description = description_str
    return description_text

def scrape_other(label, soup):
    dom_element = soup.find(string=label)
    if(dom_element is not None): return dom_element.next.get_text()
    else: return " "

def scrape_spell(website):
    result = requests.get(website)
    content = result.text
    soup = BeautifulSoup(content,'lxml')

    spell_obj = Spell()

    spell_name = soup.find('span', class_='k-icon likeButton').next_sibling.string
    spell_obj.name = spell_name
    spell_obj.actions = scrape_actions(soup)
    trait_list = scrape_traits(soup)
    spell_obj.school = trait_list[0]
    spell_obj.traits = trait_list[1]
    spell_obj.traditions = scrape_traditions(soup)
    spell_obj.deities = scrape_deities(soup)
    spell_obj.cast = scrape_cast_type(soup)
    spell_obj.requirement = scrape_other("Requirements",soup)
    spell_obj.trigger = scrape_other("Trigger",soup)
    spell_obj.cost = scrape_other("Cost",soup)
    spell_obj.range = scrape_other("Range",soup)
    spell_obj.target = scrape_other("Targets",soup)
    spell_obj.area = scrape_other("Area",soup)
    spell_obj.duration = scrape_other("Duration",soup)
    spell_obj.save_throw = scrape_other("Saving Throw",soup)
    spell_obj.description = scrape_description(soup)
    spell_obj.print_spell()

while True:
    user_input = input("Enter spell name (To exit, enter \"x\"):\n")
    if(user_input == "X" or user_input == "x"): break
    result_found = False
    query = user_input + " site:2e.aonprd.com"
    result = search(query, tld="com", num=1, start=0, stop=1, pause=2)
    for url in result: # the search function returns a list, even when instructed to find only one result.
        result_found = True
        if("https://2e.aonprd.com/Spells.aspx?ID=" in url):
            print()
            scrape_spell(url)
        else:
            print("Spell doesn't exist.\n")
    if(not result_found): print("Spell doesn't exist.\n")
