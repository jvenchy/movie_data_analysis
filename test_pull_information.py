"""
Integration tests for pull_information.py
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


class TestPullInformation(unittest.TestCase):
    """Test class for pull_information.py integration tests"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock HTML for top-rated page
        self.mock_top_rated_html = """
        <html>
            <body>
                <div class="card">
                    <h2><a href="/movie/123">The Shawshank Redemption</a></h2>
                </div>
                <div class="card">
                    <h2><a href="/movie/456">The Godfather</a></h2>
                </div>
                <div class="card">
                    <h2><a href="/movie/789">The Dark Knight</a></h2>
                </div>
            </body>
        </html>
        """

        # Mock HTML for movie detail pages
        self.mock_movie_details = {
            '/movie/123': """
            <html>
                <body>
                    <h2><a>The Shawshank Redemption</a></h2>
                    <span class="genres">
                        <a>Drama</a>
                        <a>Crime</a>
                    </span>
                    <ul>
                        <li class="profile">
                            <p>Frank Darabont</p>
                            <p class="character">Director</p>
                        </li>
                    </ul>
                    <div class="percent">
                        <span class="rating90">90%</span>
                    </div>
                </body>
            </html>
            """,
            '/movie/456': """
            <html>
                <body>
                    <h2><a>The Godfather</a></h2>
                    <span class="genres">
                        <a>Crime</a>
                        <a>Drama</a>
                    </span>
                    <ul>
                        <li class="profile">
                            <p>Francis Ford Coppola</p>
                            <p class="character">Director</p>
                        </li>
                    </ul>
                    <div class="percent">
                        <span class="rating92">92%</span>
                    </div>
                </body>
            </html>
            """,
            '/movie/789': """
            <html>
                <body>
                    <h2><a>The Dark Knight</a></h2>
                    <span class="genres">
                        <a>Action</a>
                        <a>Crime</a>
                        <a>Drama</a>
                    </span>
                    <ul>
                        <li class="profile">
                            <p>Christopher Nolan</p>
                            <p class="character">Director</p>
                        </li>
                        <li class="profile">
                            <p>John Smith</p>
                            <p class="character">Producer</p>
                        </li>
                    </ul>
                    <div class="percent">
                        <span class="rating88">88%</span>
                    </div>
                </body>
            </html>
            """
        }

    def mock_requests_get(self, url, headers=None):
        """Mock requests.get function"""
        mock_response = MagicMock()
        
        if 'top-rated' in url:
            mock_response.text = self.mock_top_rated_html
        else:
            # Extract movie URL path from full URL
            for path, html in self.mock_movie_details.items():
                if path in url:
                    mock_response.text = html
                    break
        
        return mock_response

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_pull_and_create_normal_case(self, mock_csv_writer, mock_file, mock_get):
        """Test pull_and_create with normal input"""
        # Setup mock responses
        mock_get.side_effect = self.mock_requests_get
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify CSV file was opened correctly
        mock_file.assert_called_once_with('movies.csv', 'w', newline='', encoding='utf-8')
        
        # Verify header was written
        mock_writer.writerow.assert_any_call(['Title', 'Genre(s)', 'Director(s)', 'Rating'])
        
        # Verify movie data was written
        expected_calls = [
            unittest.mock.call(['Title', 'Genre(s)', 'Director(s)', 'Rating']),
            unittest.mock.call(['The Shawshank Redemption', 'Drama, Crime', 'Frank Darabont', '90']),
            unittest.mock.call(['The Godfather', 'Crime, Drama', 'Francis Ford Coppola', '92']),
            unittest.mock.call(['The Dark Knight', 'Action, Crime, Drama', 'Christopher Nolan', '88']),
        ]
        mock_writer.writerow.assert_has_calls(expected_calls, any_order=False)
        
        # Verify number of requests made (1 for top-rated page + 3 for movie details)
        self.assertEqual(mock_get.call_count, 4)

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_pull_and_create_with_no_movies(self, mock_csv_writer, mock_file, mock_get):
        """Test pull_and_create with empty response"""
        # Setup mock response for empty page
        empty_response = MagicMock()
        empty_response.text = "<html><body></body></html>"
        mock_get.return_value = empty_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify CSV file was opened correctly
        mock_file.assert_called_once_with('movies.csv', 'w', newline='', encoding='utf-8')
        
        # Verify only header was written, no movie data
        mock_writer.writerow.assert_called_once_with(['Title', 'Genre(s)', 'Director(s)', 'Rating'])
        self.assertEqual(mock_writer.writerow.call_count, 1)

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_pull_and_create_handles_multiple_pages(self, mock_csv_writer, mock_file, mock_get):
        """Test pull_and_create handles multiple pages correctly"""
        # Setup mock responses for multiple pages
        mock_get.side_effect = self.mock_requests_get
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function with num_pulled > 20 to test multiple pages
        pull_and_create(40)
        
        # Verify calls to requests.get include page parameters
        expected_urls = [
            'https://www.themoviedb.org/movie/top-rated?page=0&language=en-US',
            'https://www.themoviedb.org/movie/top-rated?page=1&language=en-US',
            'https://www.themoviedb.org/movie/top-rated?page=2&language=en-US',
            # Plus additional calls for movie details
        ]
        
        # Extract URLs from mock_get calls
        actual_urls = [call[0][0] for call in mock_get.call_args_list if 'top-rated' in call[0][0]]
        
        # Verify first few URLs match expected pattern
        for expected, actual in zip(expected_urls, actual_urls):
            self.assertEqual(expected, actual)

    @patch('pull_information.requests.get')
    def test_pull_and_create_handles_request_errors(self, mock_get):
        """Test pull_and_create handles request errors gracefully"""
        # Setup mock to raise exception
        mock_get.side_effect = Exception("Network error")
        
        # Call function and verify it handles the exception
        with self.assertRaises(Exception) as context:
            pull_and_create(20)
        
        self.assertIn("Network error", str(context.exception))

    @patch('pull_information.requests.get')
    @patch('builtins.open', new_callable=mock_open)
    @patch('csv.writer')
    def test_pull_and_create_handles_malformed_html(self, mock_csv_writer, mock_file, mock_get):
        """Test pull_and_create handles malformed HTML gracefully"""
        # Setup mock response with malformed HTML
        malformed_response = MagicMock()
        malformed_response.text = "<html><body><div class='card'><h2>No link here</h2></div></body></html>"
        mock_get.return_value = malformed_response
        
        # Setup CSV writer mock
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer
        
        # Call the function
        pull_and_create(20)
        
        # Verify only header was written, no movie data (since HTML was malformed)
        mock_writer.writerow.assert_called_once_with(['Title', 'Genre(s)', 'Director(s)', 'Rating'])
        self.assertEqual(mock_writer.writerow.call_count, 1)


if __name__ == '__main__':
    unittest.main()
