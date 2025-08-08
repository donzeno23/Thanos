"""File discovery implementations."""

from pathlib import Path
from typing import List
import fnmatch
import re

from .interfaces import FileDiscoverer


class GlobFileDiscoverer(FileDiscoverer):
    """File discoverer using glob patterns."""
    
    def __init__(self, recursive: bool = True):
        self.recursive = recursive
    
    def discover_files(self, directory: Path, pattern: str) -> List[Path]:
        """Discover files using glob pattern matching."""
        if not directory.exists() or not directory.is_dir():
            return []
        
        if self.recursive:
            return list(directory.rglob(pattern))
        else:
            return list(directory.glob(pattern))


class FilteredFileDiscoverer(FileDiscoverer):
    """File discoverer with custom filtering logic."""
    
    def __init__(self, extensions: set[str] = None, exclude_patterns: set[str] = None):
        self.extensions = extensions or {'.py'}
        self.exclude_patterns = exclude_patterns or {'__pycache__', '.git', '.pytest_cache'}
    
    def discover_files(self, directory: Path, pattern: str) -> List[Path]:
        """Discover files with filtering."""
        files = []
        
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Check extension
            if file_path.suffix not in self.extensions:
                continue
            
            # Check exclude patterns
            if any(exclude in str(file_path) for exclude in self.exclude_patterns):
                continue
            
            # Check pattern match
            if fnmatch.fnmatch(file_path.name, pattern):
                files.append(file_path)
        



class RegexFileDiscoverer(FileDiscoverer):
    """Advanced file discoverer using regex patterns for path matching.
    
    Supports complex path patterns like 'ets/*/project*/py3/test/*/performance/*.py'
    """
    
    def __init__(self, case_sensitive: bool = True):
        self.case_sensitive = case_sensitive
    
    def discover_files(self, directory: Path, pattern: str) -> List[Path]:
        """Discover files using regex pattern matching on full paths.
        
        Args:
            directory: Root directory to search
            pattern: Regex pattern to match against relative paths
                    Examples:
                    - 'ets/*/project*/py3/test/*/performance/*.py'
                    - 'app/.*/test.*\.py$'
                    - '.*test.*\.py$'
        
        Returns:
            List of matching file paths
        """
        if not directory.exists() or not directory.is_dir():
            return []
        
        # Convert glob-style wildcards to regex if needed
        regex_pattern = self._convert_pattern_to_regex(pattern)
        
        # Compile regex pattern
        flags = 0 if self.case_sensitive else re.IGNORECASE
        try:
            compiled_pattern = re.compile(regex_pattern, flags)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern '{pattern}': {e}")
        
        matching_files = []
        
        # Walk through all files recursively
        for file_path in directory.rglob('*'):
            if not file_path.is_file():
                continue
            
            # Get relative path from directory
            try:
                relative_path = file_path.relative_to(directory)
                relative_path_str = str(relative_path).replace('\\', '/')  # Normalize path separators
                
                # Check if path matches pattern
                if compiled_pattern.match(relative_path_str) or compiled_pattern.search(relative_path_str):
                    matching_files.append(file_path)
            except ValueError:
                # Skip files outside the directory
                continue
        
        return matching_files
    
    def _convert_pattern_to_regex(self, pattern: str) -> str:
        """Convert glob-style pattern to regex if needed.
        
        Args:
            pattern: Input pattern (can be glob-style or regex)
            
        Returns:
            Regex pattern string
        """
        # If pattern already looks like regex (contains regex special chars), return as-is
        regex_chars = {'^', '$', '[', ']', '(', ')', '{', '}', '+', '?', '|', '\\'}
        if any(char in pattern for char in regex_chars):
            return pattern
        
        # Convert glob-style wildcards to regex
        # Escape regex special characters first
        escaped = re.escape(pattern)
        
        # Convert escaped glob patterns back to regex
        regex_pattern = escaped.replace(r'\*', '[^/]*')  # * matches anything except path separator
        regex_pattern = regex_pattern.replace(r'\?', '[^/]')  # ? matches single char except path separator
        
        # Handle ** for recursive directory matching
        regex_pattern = regex_pattern.replace('[^/]*/[^/]*', '.*')
        
        return regex_pattern