"""
Unit tests for analysis.py functions
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import analysis module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis import highest_rated_director, highest_rated_genre, highest_rated_director_by_genre, highest_rated_genre_by_director


class TestAnalysisFunctions(unittest.TestCase):
    """Test class for analysis.py functions"""
    
    def setUp(self):
        """Set up test data"""
        # Mock data for testing
        self.test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action, Drama', 'Director(s)': 'Director1, Director2', 'Rating': '80'},
            {'Title': 'Movie2', 'Genre(s)': 'Action, Comedy', 'Director(s)': 'Director1', 'Rating': '90'},
            {'Title': 'Movie3', 'Genre(s)': 'Drama', 'Director(s)': 'Director3', 'Rating': '85'},
            {'Title': 'Movie4', 'Genre(s)': 'Comedy', 'Director(s)': 'Director2', 'Rating': '75'},
            {'Title': 'Movie5', 'Genre(s)': 'Sci-Fi', 'Director(s)': 'Director3', 'Rating': '95'},
            {'Title': 'Movie6', 'Genre(s)': 'Action, Sci-Fi', 'Director(s)': 'Director1', 'Rating': '70'},
        ]
        
        # Create patch for the data variable in analysis module
        self.data_patcher = patch('analysis.data', self.test_data)
        self.data_patcher.start()
    
    def tearDown(self):
        """Clean up after tests"""
        self.data_patcher.stop()

    def test_highest_rated_director_normal_case(self):
        """Test highest_rated_director with valid minimum_num"""
        # Director1 has 3 movies with average rating (80 + 90 + 70) / 3 = 80
        result = highest_rated_director(2)
        self.assertEqual(result[0], 'Director1')
        self.assertAlmostEqual(result[1], 80.0)
    
    def test_highest_rated_director_tie_case(self):
        """Test highest_rated_director when directors have same average rating"""
        # Modified test data for a tie situation
        with patch('analysis.data', [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '85'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director1', 'Rating': '85'},
            {'Title': 'Movie3', 'Genre(s)': 'Comedy', 'Director(s)': 'Director2', 'Rating': '85'},
            {'Title': 'Movie4', 'Genre(s)': 'Action', 'Director(s)': 'Director2', 'Rating': '85'},
        ]):
            result = highest_rated_director(2)
            # Should pick the first director alphabetically (not specified in code, but let's verify behavior)
            self.assertIn(result[0], ['Director1', 'Director2'])
            self.assertAlmostEqual(result[1], 85.0)
    
    def test_highest_rated_director_minimum_exceeds_available(self):
        """Test highest_rated_director when minimum_num exceeds available data"""
        result = highest_rated_director(10)
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 0)
    
    def test_highest_rated_genre_normal_case(self):
        """Test highest_rated_genre with valid minimum_num"""
        # Sci-Fi appears in 2 movies with average rating (95 + 70) / 2 = 82.5
        result = highest_rated_genre(2)
        self.assertEqual(result[0], 'Action')  # Action appears in 3 movies
        self.assertAlmostEqual(result[1], 80.0)  # (80 + 90 + 70) / 3 = 80
        self.assertEqual(result[2], 'Had 3 top movies')
    
    def test_highest_rated_genre_minimum_exceeds_available(self):
        """Test highest_rated_genre when minimum_num exceeds available data"""
        result = highest_rated_genre(10)
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 'Had 0 top movies')
    
    def test_highest_rated_director_by_genre_normal_case(self):
        """Test highest_rated_director_by_genre with valid minimum_num and genre"""
        # Director1 has 2 movies in 'Action' genre with average rating (80 + 90 + 70) / 3 = 80
        result = highest_rated_director_by_genre(2, 'Action')
        self.assertEqual(result[0], 'Director1')
        self.assertEqual(result[1], 'Action')
        self.assertAlmostEqual(result[2], 80.0)
    
    def test_highest_rated_director_by_genre_invalid_genre(self):
        """Test highest_rated_director_by_genre with invalid genre"""
        result = highest_rated_director_by_genre(1, 'NonexistentGenre')
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 'NonexistentGenre')
        self.assertEqual(result[2], 0)
    
    def test_highest_rated_director_by_genre_minimum_exceeds_available(self):
        """Test highest_rated_director_by_genre when minimum_num exceeds available data"""
        result = highest_rated_director_by_genre(5, 'Action')
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 'Action')
        self.assertEqual(result[2], 0)
    
    def test_highest_rated_genre_by_director_normal_case(self):
        """Test highest_rated_genre_by_director with valid minimum_num and director"""
        # Director1 has 2 'Action' movies with average rating of (80 + 90 + 70) / 3 = 80
        result = highest_rated_genre_by_director(2, 'Director1')
        self.assertEqual(result[0], 'Action')
        self.assertEqual(result[1], 'Director1')
        self.assertAlmostEqual(result[2], 80.0)
        self.assertEqual(result[3], 'Had 3 top movies')  # Director1 has 3 Action movies
    
    def test_highest_rated_genre_by_director_invalid_director(self):
        """Test highest_rated_genre_by_director with invalid director"""
        result = highest_rated_genre_by_director(1, 'NonexistentDirector')
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 'NonexistentDirector')
        self.assertEqual(result[2], 0)
        self.assertEqual(result[3], 'Had 0 top movies')
    
    def test_highest_rated_genre_by_director_minimum_exceeds_available(self):
        """Test highest_rated_genre_by_director when minimum_num exceeds available data"""
        result = highest_rated_genre_by_director(5, 'Director1')
        self.assertEqual(result[0], 'Try a lower minimum num!')
        self.assertEqual(result[1], 'Director1')
        self.assertEqual(result[2], 0)
        self.assertEqual(result[3], 'Had 0 top movies')
    
    def test_highest_rated_director_edge_case_zero_minimum(self):
        """Test highest_rated_director with minimum_num=0"""
        # Should pick highest rated director regardless of number of movies
        result = highest_rated_director(0)
        self.assertEqual(result[0], 'Director3')  
        self.assertAlmostEqual(result[1], 90.0)  # (85 + 95) / 2 = 90
    
    def test_highest_rated_genre_edge_case_zero_minimum(self):
        """Test highest_rated_genre with minimum_num=0"""
        # Should pick highest rated genre regardless of number of movies
        result = highest_rated_genre(0)
        self.assertEqual(result[0], 'Sci-Fi')
        self.assertAlmostEqual(result[1], 82.5)  # (95 + 70) / 2 = 82.5
        self.assertEqual(result[2], 'Had 2 top movies')

    def test_highest_rated_genre_edge_case_single_movie(self):
        """Test highest_rated_genre when genre appears in only one movie"""
        with patch('analysis.data', [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '90'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director2', 'Rating': '80'},
        ]):
            result = highest_rated_genre(1)
            self.assertEqual(result[0], 'Action')
            self.assertAlmostEqual(result[1], 90.0)
            self.assertEqual(result[2], 'Had 1 top movies')


if __name__ == '__main__':
    unittest.main()
