"""
Edge case tests for analysis.py functions
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import analysis module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analysis import highest_rated_director, highest_rated_genre, highest_rated_director_by_genre, highest_rated_genre_by_director


class TestAnalysisEdgeCases(unittest.TestCase):
    """Test class for edge cases in analysis.py functions"""
    
    def test_empty_dataset(self):
        """Test functions with an empty dataset"""
        with patch('analysis.data', []):
            # Test all functions with empty data
            self.assertEqual(highest_rated_director(1), ('Try a lower minimum num!', 0))
            
            genre_result = highest_rated_genre(1)
            self.assertEqual(genre_result[0], 'Try a lower minimum num!')
            self.assertEqual(genre_result[1], 0)
            
            director_by_genre_result = highest_rated_director_by_genre(1, 'Action')
            self.assertEqual(director_by_genre_result[0], 'Try a lower minimum num!')
            self.assertEqual(director_by_genre_result[1], 'Action')
            self.assertEqual(director_by_genre_result[2], 0)
            
            genre_by_director_result = highest_rated_genre_by_director(1, 'Director1')
            self.assertEqual(genre_by_director_result[0], 'Try a lower minimum num!')
            self.assertEqual(genre_by_director_result[1], 'Director1')
            self.assertEqual(genre_by_director_result[2], 0)
            self.assertEqual(genre_by_director_result[3], 'Had 0 top movies')
    
    def test_negative_minimum_num(self):
        """Test functions with negative minimum_num parameter"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '80'},
        ]
        
        with patch('analysis.data', test_data):
            # Negative minimum_num should be treated as 0
            director_result = highest_rated_director(-1)
            self.assertEqual(director_result[0], 'Director1')
            self.assertAlmostEqual(director_result[1], 80.0)
            
            genre_result = highest_rated_genre(-1)
            self.assertEqual(genre_result[0], 'Action')
            self.assertAlmostEqual(genre_result[1], 80.0)
    
    def test_zero_ratings(self):
        """Test functions with zero ratings"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '0'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director1', 'Rating': '0'},
        ]
        
        with patch('analysis.data', test_data):
            director_result = highest_rated_director(1)
            self.assertEqual(director_result[0], 'Director1')
            self.assertAlmostEqual(director_result[1], 0.0)
    
    def test_extremely_high_ratings(self):
        """Test functions with extremely high ratings"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '999'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director2', 'Rating': '100'},
        ]
        
        with patch('analysis.data', test_data):
            director_result = highest_rated_director(1)
            self.assertEqual(director_result[0], 'Director1')
            self.assertAlmostEqual(director_result[1], 999.0)
    
    def test_empty_genres_and_directors(self):
        """Test functions with empty genres and directors"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': '', 'Director(s)': '', 'Rating': '80'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director1', 'Rating': '90'},
        ]
        
        with patch('analysis.data', test_data):
            # Empty genre shouldn't be counted
            genre_result = highest_rated_genre(1)
            self.assertEqual(genre_result[0], 'Drama')
            
            # Empty director shouldn't be counted
            director_result = highest_rated_director(1)
            self.assertEqual(director_result[0], 'Director1')
    
    def test_unicode_characters(self):
        """Test functions with unicode characters in genres and directors"""
        test_data = [
            {'Title': 'Amélie', 'Genre(s)': 'Comédie, Romance', 'Director(s)': 'Jean-Pierre Jeunet', 'Rating': '90'},
            {'Title': 'Crouching Tiger, Hidden Dragon', 'Genre(s)': 'Action, 武术', 'Director(s)': '李安', 'Rating': '95'},
        ]
        
        with patch('analysis.data', test_data):
            # Should handle unicode characters correctly
            genre_result = highest_rated_genre(1)
            self.assertIn(genre_result[0], ['Comédie', 'Romance', 'Action', '武术'])
            
            director_result = highest_rated_director(1)
            self.assertIn(director_result[0], ['Jean-Pierre Jeunet', '李安'])
    
    def test_all_directors_have_one_movie(self):
        """Test highest_rated_director when all directors have exactly one movie"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '80'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director2', 'Rating': '90'},
            {'Title': 'Movie3', 'Genre(s)': 'Comedy', 'Director(s)': 'Director3', 'Rating': '85'},
        ]
        
        with patch('analysis.data', test_data):
            # With minimum_num=1, should return Director2 with rating 90
            result = highest_rated_director(1)
            self.assertEqual(result[0], 'Director2')
            self.assertAlmostEqual(result[1], 90.0)
            
            # With minimum_num=2, should return 'Try a lower minimum num!'
            result = highest_rated_director(2)
            self.assertEqual(result[0], 'Try a lower minimum num!')
    
    def test_highest_rated_director_by_unknowngenre(self):
        """Test highest_rated_director_by_genre with a genre that doesn't exist"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '80'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director2', 'Rating': '90'},
        ]
        
        with patch('analysis.data', test_data):
            result = highest_rated_director_by_genre(1, 'Fantasy')
            self.assertEqual(result[0], 'Try a lower minimum num!')
            self.assertEqual(result[1], 'Fantasy')
            self.assertEqual(result[2], 0)
    
    def test_highest_rated_genre_by_unknown_director(self):
        """Test highest_rated_genre_by_director with a director that doesn't exist"""
        test_data = [
            {'Title': 'Movie1', 'Genre(s)': 'Action', 'Director(s)': 'Director1', 'Rating': '80'},
            {'Title': 'Movie2', 'Genre(s)': 'Drama', 'Director(s)': 'Director2', 'Rating': '90'},
        ]
        
        with patch('analysis.data', test_data):
            result = highest_rated_genre_by_director(1, 'UnknownDirector')
            self.assertEqual(result[0], 'Try a lower minimum num!')
            self.assertEqual(result[1], 'UnknownDirector')
            self.assertEqual(result[2], 0)
            self.assertEqual(result[3], 'Had 0 top movies')
    
    def test_extreme_large_dataset(self):
        """Test functions with an extremely large dataset"""
        # Create a dataset with 1000 movies, 100 directors, 20 genres
        large_dataset = []
        
        for i in range(1000):
            director_idx = i % 100
            genre_idx = i % 20
            rating = (i % 10) + 80  # ratings from 80 to 89
            
            movie = {
                'Title': f'Movie{i}',
                'Genre(s)': f'Genre{genre_idx}',
                'Director(s)': f'Director{director_idx}',
                'Rating': str(rating)
            }
            large_dataset.append(movie)
        
        with patch('analysis.data', large_dataset):
            # Each director has 10 movies
            result = highest_rated_director(10)
            self.assertIsNotNone(result[0])
            self.assertNotEqual(result[0], 'Try a lower minimum num!')
            
            # Each genre has 50 movies
            result = highest_rated_genre(50)
            self.assertIsNotNone(result[0])
            self.assertNotEqual(result[0], 'Try a lower minimum num!')


if __name__ == '__main__':
    unittest.main()
