import unittest
import Data_Scraper_Draft_2
from bs4 import BeautifulSoup
import requests

def getSoup(website):
    result = requests.get(website)
    content = result.text
    return BeautifulSoup(content,'lxml')

class TestScraper(unittest.TestCase):
    def setUp(self):
        self.soup_repulsion = getSoup('https://2e.aonprd.com/Spells.aspx?ID=254')
        self.soup_worm_sting = getSoup('https://2e.aonprd.com/Spells.aspx?ID=242')
        self.soup_raise_dead = getSoup('https://2e.aonprd.com/Spells.aspx?ID=243')
        self.soup_dino_fort = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1099')
        self.soup_acid_splash = getSoup('https://2e.aonprd.com/Spells.aspx?ID=3')
        self.soup_quick_sort = getSoup('https://2e.aonprd.com/Spells.aspx?ID=978')
        self.soup_eat_fire = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1352')
        self.soup_chill_touch = getSoup('https://2e.aonprd.com/Spells.aspx?ID=35')
        self.soup_alarm = getSoup('https://2e.aonprd.com/Spells.aspx?ID=7')
        self.soup_bread_crumbs = getSoup('https://2e.aonprd.com/Spells.aspx?ID=876')
        self.soup_frost_ray = getSoup('https://2e.aonprd.com/Spells.aspx?ID=245')
        self.soup_know_dir = getSoup('https://2e.aonprd.com/Spells.aspx?ID=169')
        self.soup_time_sense = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1193')
        self.soup_jump = getSoup('https://2e.aonprd.com/Spells.aspx?ID=167')
        self.soup_deep_breath = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1315')
        self.soup_summon_instrument = getSoup('https://2e.aonprd.com/Spells.aspx?ID=721')
        self.soup_animate_dead = getSoup('https://2e.aonprd.com/Spells.aspx?ID=666')
        self.soup_choir = getSoup('https://2e.aonprd.com/Spells.aspx?ID=886')
        self.soup_exchange_image = getSoup('https://2e.aonprd.com/Spells.aspx?ID=549') # Requirements edge case -- it has links in description
        self.soup_feather_fall = getSoup('https://2e.aonprd.com/Spells.aspx?ID=111')
        self.soup_gravity_pull = getSoup('https://2e.aonprd.com/Spells.aspx?ID=921')
        self.soup_harm = getSoup('https://2e.aonprd.com/Spells.aspx?ID=146')
        self.soup_thunder_sphere = getSoup('https://2e.aonprd.com/Spells.aspx?ID=927')
        self.soup_lose_path = getSoup('https://2e.aonprd.com/Spells.aspx?ID=940')
        self.soup_spirit_torrent = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1267')
        self.soup_element_breath = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1420')
        self.soup_chrom_armor = getSoup('https://2e.aonprd.com/Spells.aspx?ID=881')

        # trigger edge cases
        self.soup_element_counter = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1421')
        # another edge case is 'https://2e.aonprd.com/Spells.aspx?ID=997'  shift blame
        # 'https://2e.aonprd.com/Spells.aspx?ID=1319'

        # description edge case (contains bullet pts)
        self.soup_righteous_might = getSoup('https://2e.aonprd.com/Spells.aspx?ID=263') 
        self.soup_chromatic_image = getSoup('https://2e.aonprd.com/Spells.aspx?ID=882')
        self.soup_variable_gravity = getSoup('https://2e.aonprd.com/Spells.aspx?ID=1026')
        self.soup_fey_form = getSoup('https://2e.aonprd.com/Spells.aspx?ID=910')
        self.soup_gift = getSoup('https://2e.aonprd.com/Spells.aspx?ID=904')

        # cost test
        self.soup_holy_cascade = getSoup('https://2e.aonprd.com/Spells.aspx?ID=151')
        # 'https://2e.aonprd.com/Spells.aspx?ID=859'  mind games

        # it has another spell within the description -- 'https://2e.aonprd.com/Spells.aspx?ID=939' life connection
        # 'https://2e.aonprd.com/Spells.aspx?ID=1011'  -- summonors precaution

    def test_scrape_actions(self):
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_eat_fire),"Reaction")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_feather_fall),"Reaction")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_lose_path),"Reaction") 

        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_time_sense),"Single action")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_jump),"Single action")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_deep_breath),"Single action")

        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_choir),"One to three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_gravity_pull),"One to three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_harm),"One to three actions")

        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_repulsion),"Two actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_frost_ray),"Two actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_know_dir),"Two actions")

        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_spirit_torrent),"Two or three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_element_breath),"Two or three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_chrom_armor),"Two or three actions")

        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_quick_sort),"Three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_summon_instrument),"Three actions")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_animate_dead),"Three actions")

        # TODO: find a way to get rid of the two spaces after Cast Time:
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_raise_dead),"Cast Time:  10 minutes")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_alarm),"Cast Time:  10 minutes")
        self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_bread_crumbs),"Cast Time:  1 minute")

        # # TODO: Add this new case to Data_Scraper_Draft_2
        # self.assertEqual(Data_Scraper_Draft_2.scrape_actions(self.soup_thunder_sphere),"Two actions to 2 rounds")
        # # another edge case : 'https://2e.aonprd.com/Spells.aspx?ID=902'  annihilation wave == two actions to 2 rounds
        # # 'https://2e.aonprd.com/Spells.aspx?ID=934'

    def test_scrape_traits(self):
        # I tested for the following edge cases: No school of magic, one school of magic (a spell can't have multiple schools) no traits, one trait, several traits
        # TODO: test for every school of magic, which includes "Abjuration","Conjuration","Divination","Enchantment","Evocation","Illusion","Necromancy","Transmutation"
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_acid_splash), ['Evocation', ['Acid', 'Attack', 'Cantrip']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_alarm), ['Abjuration',[]])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_animate_dead),['Necromancy',[]])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_bread_crumbs),['Abjuration', []])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_chill_touch),['Necromancy', ['Cantrip', 'Negative']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_choir), ['Evocation', ['Sonic']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_chrom_armor), ['Abjuration', ['Light']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_chromatic_image), ['Illusion', ['Visual']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_deep_breath), ['', ['Air', 'Cantrip', 'Manipulate']])
        self.assertEqual(Data_Scraper_Draft_2.scrape_traits(self.soup_dino_fort), ['Conjuration', ['Rare']])


if __name__ == '__main__':
    unittest.main()
        
