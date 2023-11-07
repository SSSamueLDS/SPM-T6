import unittest
import json
from main import SkillMatchPercentage, isListingExpired, userHasSkill, truncateDescription, sort_alphabetically, sort_by_ID, process_listing_name
from datetime import date

class TestSkillMatchPercentage(unittest.TestCase):
    def setUp(self):
        self.skillrequired =[1,2,3,4,5,6,7,8,9,10]
        self.employeeskill = [1,2,3,4,5,6,7,8,9]
    def tearDown(self) -> None:
        return super().tearDown()
    def test_skill_match_percentage(self):
        self.assertEqual(90, SkillMatchPercentage(self.skillrequired, self.employeeskill))
        
class TestIsListingExpired(unittest.TestCase):
    def setUp(self):
        self.listingDeadline = "2025-01-01"
        self.today = date.today()
    def tearDown(self) -> None:
        return super().tearDown()
    def test_is_listing_expired(self):
        self.assertEqual(False, isListingExpired(self.listingDeadline))
    
class TestuserHasSkill(unittest.TestCase):
    def setUp(self):
        self.userSkill = [1,2,3,4,5,6,7,8,9]
        self.skillID = 1
    def tearDown(self) -> None:
        return super().tearDown()
    def test_user_has_skill(self):
        self.assertEqual(True, userHasSkill(self.skillID, self.userSkill))

class TestsortAlphabetically(unittest.TestCase):    
    def setUp(self):
        self.skills = [{"id": 1, "skill_name": "R"}, {"id": 2, "skill_name": "Java"}, {"id": 3, "skill_name": "Python"}]
    def tearDown(self) -> None:
        return super().tearDown()
    def test_sort_alphabetically(self):
        self.assertEqual([{"id": 2, "skill_name": "Java"}, {"id": 3, "skill_name": "Python"}, {"id": 1, "skill_name": "R"}], sort_alphabetically(self.skills))
    
class TestsortByID(unittest.TestCase):
    def setUp(self):
        self.skills = [{"id": 5, "skill_name": "R"}, {"id": 2, "skill_name": "Java"}, {"id": 3, "skill_name": "Python"}]
    def tearDown(self) -> None:
        return super().tearDown()
    def test_sort_by_ID(self):
        self.assertEqual([{"id": 2, "skill_name": "Java"}, {"id": 3, "skill_name": "Python"}, {"id": 5, "skill_name": "R"}], sort_by_ID(self.skills))



class TesttruncateDescription(unittest.TestCase):
    def setUp(self):
        self.description= "This is a very long description with more than 100 words. It's just a sample text to demonstrate the behavior of the truncateDescription function. This text continues to add more words to ensure it exceeds 100 words. The purpose is to test the truncation functionality."
    def tearDown(self) -> None:
        return super().tearDown()
    def test_truncate_description(self):
        self.maxDiff = None
        truncated_result = " ".join(self.description.split()[:100])
        self.assertEqual(truncated_result, truncateDescription(self.description))

class TestProcessListingName(unittest.TestCase):
    def setUp(self):
        self.listing_name = "hello123$%^&*()_+ilovespm"
    def tearDown(self) -> None:
        return super().tearDown()
    def test_process_listing_name(self):
        self.assertEqual("hello123ilovespm", process_listing_name(self.listing_name))
 
if __name__ == '__main__':
   unittest.main()