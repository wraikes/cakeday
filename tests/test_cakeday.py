import pytest
import sys
import os
from io import StringIO
from unittest.mock import patch, MagicMock

# Add the src directory to the path to import cakeday modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'cakeday'))

import cakeday
from operations import get_all, get_by_name


class TestDisplayMenu:
    """Test cases for display_menu function"""
    
    def test_display_menu_output(self, capsys):
        """Test that display_menu prints the correct menu"""
        cakeday.display_menu()
        captured = capsys.readouterr()
        
        expected_lines = [
            "=== Birthday Manager ===",
            "1. Create new birthday record",
            "2. View all birthdays",
            "3. Search for specific birthday",
            "4. Update existing birthday",
            "5. Delete birthday record",
            "6. Exit",
            "========================"
        ]
        
        for line in expected_lines:
            assert line in captured.out


class TestViewAllBirthdays:
    """Test cases for view_all_birthdays function"""
    
    @patch('cakeday.get_all')
    def test_view_all_birthdays_no_records(self, mock_get_all, capsys):
        """Test view_all_birthdays when no records exist"""
        mock_get_all.return_value = []
        
        cakeday.view_all_birthdays()
        captured = capsys.readouterr()
        
        assert "No birthday records found." in captured.out
    
    @patch('cakeday.get_all')
    def test_view_all_birthdays_with_records(self, mock_get_all, capsys):
        """Test view_all_birthdays with sample records"""
        mock_get_all.return_value = [
            ("John Doe", "01-15", "y", 14),
            ("Jane Smith", "06-30", "n", 0)
        ]
        
        cakeday.view_all_birthdays()
        captured = capsys.readouterr()
        
        assert "All Birthday Records:" in captured.out
        assert "John Doe" in captured.out
        assert "01-15" in captured.out
        assert "Jane Smith" in captured.out
        assert "06-30" in captured.out


class TestSearchBirthday:
    """Test cases for search_birthday function"""
    
    @patch('builtins.input', return_value="")
    def test_search_birthday_empty_name(self, mock_input, capsys):
        """Test search_birthday with empty name input"""
        cakeday.search_birthday()
        captured = capsys.readouterr()
        
        assert "Name cannot be empty" in captured.out
    
    @patch('builtins.input', return_value="John Doe")
    @patch('cakeday.get_by_name')
    def test_search_birthday_not_found(self, mock_get_by_name, mock_input, capsys):
        """Test search_birthday when record is not found"""
        mock_get_by_name.return_value = None
        
        cakeday.search_birthday()
        captured = capsys.readouterr()
        
        assert "No record found for John Doe" in captured.out
    
    @patch('builtins.input', return_value="John Doe")
    @patch('cakeday.get_by_name')
    def test_search_birthday_found(self, mock_get_by_name, mock_input, capsys):
        """Test search_birthday when record is found"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        
        cakeday.search_birthday()
        captured = capsys.readouterr()
        
        assert "Record found:" in captured.out
        assert "Name: John Doe" in captured.out
        assert "Birthday: 01-15" in captured.out
        assert "Notifications: y" in captured.out
        assert "Advance Days: 14" in captured.out


class TestMainFunction:
    """Test cases for main function"""
    
    @patch('builtins.input', return_value="6")
    def test_main_exit_choice(self, mock_input, capsys):
        """Test main function with exit choice"""
        cakeday.main()
        captured = capsys.readouterr()
        
        assert "Goodbye, and thanks for all the fish!" in captured.out
    
    @patch('builtins.input', return_value="7")
    def test_main_invalid_choice(self, mock_input, capsys):
        """Test main function with invalid choice"""
        with patch('builtins.input', side_effect=["7", "6"]):
            cakeday.main()
            captured = capsys.readouterr()
            
            assert "Invalid choice. Please enter a number between 1 and 6." in captured.out
    
    @patch('builtins.input', side_effect=KeyboardInterrupt)
    def test_main_keyboard_interrupt(self, mock_input, capsys):
        """Test main function handles KeyboardInterrupt"""
        cakeday.main()
        captured = capsys.readouterr()
        
        assert "Goodbye!" in captured.out
    
    @patch('builtins.input', return_value="1")
    @patch('cakeday.create')
    def test_main_create_choice(self, mock_create, mock_input):
        """Test main function calls create function"""
        with patch('builtins.input', side_effect=["1", "6"]):
            cakeday.main()
            mock_create.assert_called_once()
    
    @patch('builtins.input', return_value="2")
    @patch('cakeday.view_all_birthdays')
    def test_main_view_all_choice(self, mock_view_all, mock_input):
        """Test main function calls view_all_birthdays function"""
        with patch('builtins.input', side_effect=["2", "6"]):
            cakeday.main()
            mock_view_all.assert_called_once()
    
    @patch('builtins.input', return_value="3")
    @patch('cakeday.search_birthday')
    def test_main_search_choice(self, mock_search, mock_input):
        """Test main function calls search_birthday function"""
        with patch('builtins.input', side_effect=["3", "6"]):
            cakeday.main()
            mock_search.assert_called_once()
    
    @patch('builtins.input', return_value="4")
    @patch('cakeday.update')
    def test_main_update_choice(self, mock_update, mock_input):
        """Test main function calls update function"""
        with patch('builtins.input', side_effect=["4", "6"]):
            cakeday.main()
            mock_update.assert_called_once()
    
    @patch('builtins.input', return_value="5")
    @patch('cakeday.delete')
    def test_main_delete_choice(self, mock_delete, mock_input):
        """Test main function calls delete function"""
        with patch('builtins.input', side_effect=["5", "6"]):
            cakeday.main()
            mock_delete.assert_called_once()
    
    @patch('builtins.input', return_value="1")
    @patch('cakeday.create', side_effect=Exception("Test error"))
    def test_main_exception_handling(self, mock_create, mock_input, capsys):
        """Test main function handles exceptions"""
        with patch('builtins.input', side_effect=["1", "6"]):
            cakeday.main()
            captured = capsys.readouterr()
            
            assert "An error occurred: Test error" in captured.out