"""
Edge case integration tests for pull_information.py
"""
import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import csv
import io

# Add parent directory to path to import pull_information module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pull_information import pull_and_create


class TestPullInformationEdgeCases(unittest.TestCase):
    """Test class for edge cases in pull_information.py"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock HTML for top-rated page
        self.mock_top_rated_html = """
        <html><body>
            <div class="card"><h2><a href="/movie/123">Normal Movie</a></h2></div>
        </body></html>
        """

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_movie_missing_director(self, mock_csv_writer, mock_file, mock_get):
        """Test handling of movie pages with missing director information"""
        # Movie page with no director information
        no_director_html = """
        <html><body>
            <h2><a>No Director Movie</a></h2>
            <span class="genres"><a>Drama</a></span>
            <div class="percent"><span class="rating85">85%</span></div>
        </body></html>
        """
        
        # Setup mock responses
        def mock_get_response(url, headers=None):
            response = MagicMock()
            if 'top-rated' in url:
                response.text = self.mock_top_rated_html
            else:
                response.text = no_director_html
            return response
        
        mock_get.side_effect = mock_get_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify movie data was written with empty director
        mock_writer.writerow.assert_any_call(['No Director Movie', 'Drama', '', '85'])

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_movie_missing_rating(self, mock_csv_writer, mock_file, mock_get):
        """Test handling of movie pages with missing rating information"""
        # Movie page with no rating information
        no_rating_html = """
        <html><body>
            <h2><a>No Rating Movie</a></h2>
            <span class="genres"><a>Drama</a></span>
            <ul>
                <li class="profile">
                    <p>John Doe</p>
                    <p class="character">Director</p>
                </li>
            </ul>
            <div class="percent"></div>
        </body></html>
        """
        
        # Setup mock responses
        def mock_get_response(url, headers=None):
            response = MagicMock()
            if 'top-rated' in url:
                response.text = self.mock_top_rated_html
            else:
                response.text = no_rating_html
            return response
        
        mock_get.side_effect = mock_get_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function - should handle the error without writing this movie
        with self.assertRaises(AttributeError):
            pull_and_create(20)

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_movie_with_multiple_directors(self, mock_csv_writer, mock_file, mock_get):
        """Test handling of movies with multiple directors"""
        # Movie page with multiple directors
        multi_director_html = """
        <html><body>
            <h2><a>Multi-Director Movie</a></h2>
            <span class="genres"><a>Action</a></span>
            <ul>
                <li class="profile">
                    <p>Director One</p>
                    <p class="character">Director</p>
                </li>
                <li class="profile">
                    <p>Director Two</p>
                    <p class="character">Director</p>
                </li>
            </ul>
            <div class="percent"><span class="rating90">90%</span></div>
        </body></html>
        """
        
        # Setup mock responses
        def mock_get_response(url, headers=None):
            response = MagicMock()
            if 'top-rated' in url:
                response.text = self.mock_top_rated_html
            else:
                response.text = multi_director_html
            return response
        
        mock_get.side_effect = mock_get_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify movie data was written with both directors
        mock_writer.writerow.assert_any_call(['Multi-Director Movie', 'Action', 'Director One, Director Two', '90'])

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_movie_with_unicode_characters(self, mock_csv_writer, mock_file, mock_get):
        """Test handling of movies with Unicode characters"""
        # Movie page with Unicode characters
        unicode_html = """
        <html><body>
            <h2><a>Amélie</a></h2>
            <span class="genres"><a>Comédie</a></span>
            <ul>
                <li class="profile">
                    <p>Jean-Pierre Jeunet</p>
                    <p class="character">Director</p>
                </li>
            </ul>
            <div class="percent"><span class="rating92">92%</span></div>
        </body></html>
        """
        
        # Setup mock responses
        def mock_get_response(url, headers=None):
            response = MagicMock()
            if 'top-rated' in url:
                response.text = self.mock_top_rated_html
            else:
                response.text = unicode_html
            return response
        
        mock_get.side_effect = mock_get_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify movie data was written correctly with unicode characters
        mock_writer.writerow.assert_any_call(['Amélie', 'Comédie', 'Jean-Pierre Jeunet', '92'])

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_request_timeout(self, mock_csv_writer, mock_file, mock_get):
        """Test handling of request timeouts"""
        from requests.exceptions import Timeout
        
        # Setup mock to raise timeout
        mock_get.side_effect = Timeout("Request timed out")
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function and verify it handles the timeout
        with self.assertRaises(Timeout):
            pull_and_create(20)
        
        # Verify header was still written before exception
        mock_writer.writerow.assert_called_once_with(['Title', 'Genre(s)', 'Director(s)', 'Rating'])

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_zero_movies_requested(self, mock_csv_writer, mock_file, mock_get):
        """Test handling when requesting zero movies"""
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function with zero movies
        pull_and_create(0)
        
        # Verify only header was written, no requests made
        mock_writer.writerow.assert_called_once_with(['Title', 'Genre(s)', 'Director(s)', 'Rating'])
        mock_get.assert_not_called()

    @patch('pull_information.requests.get')
    @patch('csv.writer')
    def test_file_write_error(self, mock_csv_writer, mock_get):
        """Test handling of file write errors"""
        # Mock open to raise an error
        m = mock_open()
        m.side_effect = IOError("File write error")
        
        with patch('builtins.open', m):
            # Call the function and verify it handles the file error
            with self.assertRaises(IOError):
                pull_and_create(20)


if __name__ == '__main__':
    unittest.main()
