import pytest
import sys
import os
import sqlite3
import tempfile
from unittest.mock import patch, MagicMock, mock_open

# Add the src directory to the path to import operations
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'cakeday'))

import operations


class TestValidationFunctions:
    """Test cases for validation functions"""
    
    def test_validate_birthday_format_valid(self):
        """Test validate_birthday_format with valid inputs"""
        assert operations.validate_birthday_format("01-15") == True
        assert operations.validate_birthday_format("12-31") == True
        assert operations.validate_birthday_format("06-30") == True
    
    def test_validate_birthday_format_invalid(self):
        """Test validate_birthday_format with invalid inputs"""
        assert operations.validate_birthday_format("1-15") == False
        assert operations.validate_birthday_format("01-5") == False
        assert operations.validate_birthday_format("1-5") == False
        assert operations.validate_birthday_format("01/15") == False
        assert operations.validate_birthday_format("01-15-2023") == False
        assert operations.validate_birthday_format("invalid") == False
        assert operations.validate_birthday_format("") == False
    
    def test_validate_notification_input_valid(self):
        """Test validate_notification_input with valid inputs"""
        assert operations.validate_notification_input("y") == True
        assert operations.validate_notification_input("Y") == True
        assert operations.validate_notification_input("yes") == True
        assert operations.validate_notification_input("YES") == True
        assert operations.validate_notification_input("n") == True
        assert operations.validate_notification_input("N") == True
        assert operations.validate_notification_input("no") == True
        assert operations.validate_notification_input("NO") == True
    
    def test_validate_notification_input_invalid(self):
        """Test validate_notification_input with invalid inputs"""
        assert operations.validate_notification_input("maybe") == False
        assert operations.validate_notification_input("1") == False
        assert operations.validate_notification_input("true") == False
        assert operations.validate_notification_input("false") == False
        assert operations.validate_notification_input("") == False


class TestDatabaseFunctions:
    """Test cases for database functions"""
    
    def setup_method(self):
        """Set up test database"""
        self.test_db = tempfile.NamedTemporaryFile(delete=False)
        self.test_db.close()
        
        # Create test database with cakeday table
        conn = sqlite3.connect(self.test_db.name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE cakeday (
                name TEXT PRIMARY KEY,
                birthday TEXT,
                notification TEXT,
                adv_days INTEGER
            )
        ''')
        conn.commit()
        conn.close()
    
    def teardown_method(self):
        """Clean up test database"""
        os.unlink(self.test_db.name)
    
    @patch('operations.get_db_connection')
    def test_get_all_empty(self, mock_get_db_connection):
        """Test get_all with empty database"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        result = operations.get_all()
        
        assert result == []
        mock_cursor.execute.assert_called_once_with('SELECT * FROM cakeday ORDER BY name')
    
    @patch('operations.get_db_connection')
    def test_get_all_with_records(self, mock_get_db_connection):
        """Test get_all with records in database"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            ("John Doe", "01-15", "y", 14),
            ("Jane Smith", "06-30", "n", 0)
        ]
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        result = operations.get_all()
        
        assert len(result) == 2
        assert result[0] == ("John Doe", "01-15", "y", 14)
        assert result[1] == ("Jane Smith", "06-30", "n", 0)
    
    @patch('operations.get_db_connection')
    def test_get_by_name_found(self, mock_get_db_connection):
        """Test get_by_name when record is found"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ("John Doe", "01-15", "y", 14)
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        result = operations.get_by_name("John Doe")
        
        assert result == ("John Doe", "01-15", "y", 14)
        mock_cursor.execute.assert_called_once_with('SELECT * FROM cakeday WHERE name = ?', ("John Doe",))
    
    @patch('operations.get_db_connection')
    def test_get_by_name_not_found(self, mock_get_db_connection):
        """Test get_by_name when record is not found"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        result = operations.get_by_name("Nonexistent")
        
        assert result is None


class TestCreateFunction:
    """Test cases for create function"""
    
    @patch('builtins.input', return_value="")
    def test_create_empty_name(self, mock_input, capsys):
        """Test create with empty name"""
        operations.create()
        captured = capsys.readouterr()
        
        assert "Name cannot be empty" in captured.out
    
    @patch('builtins.input', return_value="John Doe")
    @patch('operations.get_by_name')
    def test_create_existing_name(self, mock_get_by_name, mock_input, capsys):
        """Test create with existing name"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        
        operations.create()
        captured = capsys.readouterr()
        
        assert "Record for John Doe already exists. Use update to modify." in captured.out
    
    @patch('operations.get_by_name', return_value=None)
    @patch('operations.get_db_connection')
    def test_create_success(self, mock_get_db_connection, mock_get_by_name, capsys):
        """Test successful create operation"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        with patch('builtins.input', side_effect=["John Doe", "01-15", "y", "14"]):
            operations.create()
            captured = capsys.readouterr()
            
            assert "Successfully added birthday for John Doe" in captured.out
            mock_cursor.execute.assert_called_with(
                'INSERT INTO cakeday VALUES (?, ?, ?, ?)', 
                ("John Doe", "01-15", "y", 14)
            )
    
    @patch('operations.get_by_name', return_value=None)
    def test_create_invalid_birthday_format(self, mock_get_by_name, capsys):
        """Test create with invalid birthday format"""
        with patch('builtins.input', side_effect=["John Doe", "1-15", "01-15", "y", "14"]):
            with patch('operations.get_db_connection') as mock_get_db_connection:
                mock_conn = MagicMock()
                mock_cursor = MagicMock()
                mock_conn.cursor.return_value = mock_cursor
                mock_get_db_connection.return_value.__enter__.return_value = mock_conn
                
                operations.create()
                captured = capsys.readouterr()
                
                assert "Invalid input; please try again in format mm-dd:" in captured.out
    
    @patch('operations.get_by_name', return_value=None)
    def test_create_invalid_notification_input(self, mock_get_by_name, capsys):
        """Test create with invalid notification input"""
        with patch('builtins.input', side_effect=["John Doe", "01-15", "maybe", "y", "14"]):
            with patch('operations.get_db_connection') as mock_get_db_connection:
                mock_conn = MagicMock()
                mock_cursor = MagicMock()
                mock_conn.cursor.return_value = mock_cursor
                mock_get_db_connection.return_value.__enter__.return_value = mock_conn
                
                operations.create()
                captured = capsys.readouterr()
                
                assert "Please enter 'y' for yes or 'n' for no" in captured.out
    
    @patch('operations.get_by_name', return_value=None)
    def test_create_no_notification(self, mock_get_by_name, capsys):
        """Test create with no notification preference"""
        with patch('builtins.input', side_effect=["John Doe", "01-15", "n"]):
            with patch('operations.get_db_connection') as mock_get_db_connection:
                mock_conn = MagicMock()
                mock_cursor = MagicMock()
                mock_conn.cursor.return_value = mock_cursor
                mock_get_db_connection.return_value.__enter__.return_value = mock_conn
                
                operations.create()
                captured = capsys.readouterr()
                
                assert "Successfully added birthday for John Doe" in captured.out
                mock_cursor.execute.assert_called_with(
                    'INSERT INTO cakeday VALUES (?, ?, ?, ?)', 
                    ("John Doe", "01-15", "n", 0)
                )


class TestDeleteFunction:
    """Test cases for delete function"""
    
    @patch('builtins.input', return_value="")
    def test_delete_empty_name(self, mock_input, capsys):
        """Test delete with empty name"""
        operations.delete()
        captured = capsys.readouterr()
        
        assert "Name cannot be empty" in captured.out
    
    @patch('builtins.input', return_value="Nonexistent")
    @patch('operations.get_by_name', return_value=None)
    def test_delete_not_found(self, mock_get_by_name, mock_input, capsys):
        """Test delete with non-existent name"""
        operations.delete()
        captured = capsys.readouterr()
        
        assert "No record found for Nonexistent" in captured.out
    
    @patch('operations.get_by_name')
    def test_delete_cancelled(self, mock_get_by_name, capsys):
        """Test delete operation cancelled by user"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        
        with patch('builtins.input', side_effect=["John Doe", "n"]):
            operations.delete()
            captured = capsys.readouterr()
            
            assert "Delete cancelled" in captured.out
    
    @patch('operations.get_by_name')
    @patch('operations.get_db_connection')
    def test_delete_success(self, mock_get_db_connection, mock_get_by_name, capsys):
        """Test successful delete operation"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        with patch('builtins.input', side_effect=["John Doe", "y"]):
            operations.delete()
            captured = capsys.readouterr()
            
            assert "Successfully deleted birthday for John Doe" in captured.out
            mock_cursor.execute.assert_called_with(
                'DELETE FROM cakeday WHERE name = ?', 
                ("John Doe",)
            )


class TestUpdateFunction:
    """Test cases for update function"""
    
    @patch('builtins.input', return_value="")
    def test_update_empty_name(self, mock_input, capsys):
        """Test update with empty name"""
        operations.update()
        captured = capsys.readouterr()
        
        assert "Name cannot be empty" in captured.out
    
    @patch('builtins.input', return_value="Nonexistent")
    @patch('operations.get_by_name', return_value=None)
    def test_update_not_found(self, mock_get_by_name, mock_input, capsys):
        """Test update with non-existent name"""
        operations.update()
        captured = capsys.readouterr()
        
        assert "No record found for Nonexistent" in captured.out
    
    @patch('operations.get_by_name')
    @patch('operations.get_db_connection')
    def test_update_success(self, mock_get_db_connection, mock_get_by_name, capsys):
        """Test successful update operation"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        with patch('builtins.input', side_effect=["John Doe", "02-20", "n", ""]):
            operations.update()
            captured = capsys.readouterr()
            
            assert "Successfully updated birthday for John Doe" in captured.out
            mock_cursor.execute.assert_called_with(
                'UPDATE cakeday SET birthday = ?, notification = ?, adv_days = ? WHERE name = ?', 
                ("02-20", "n", 0, "John Doe")
            )
    
    @patch('operations.get_by_name')
    @patch('operations.get_db_connection')
    def test_update_keep_existing_values(self, mock_get_db_connection, mock_get_by_name, capsys):
        """Test update keeping existing values"""
        mock_get_by_name.return_value = ("John Doe", "01-15", "y", 14)
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_db_connection.return_value.__enter__.return_value = mock_conn
        
        with patch('builtins.input', side_effect=["John Doe", "", "", ""]):
            operations.update()
            captured = capsys.readouterr()
            
            assert "Successfully updated birthday for John Doe" in captured.out
            mock_cursor.execute.assert_called_with(
                'UPDATE cakeday SET birthday = ?, notification = ?, adv_days = ? WHERE name = ?', 
                ("01-15", "y", 14, "John Doe")
            )