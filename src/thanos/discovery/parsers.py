"""AST-based parsers for test suite discovery."""

import ast
from typing import List, Set
from pathlib import Path

from .interfaces import FileParser, TestSuiteInfo


class ASTTestSuiteParser(FileParser):
    """AST-based parser for discovering test suites with decorators."""
    
    def __init__(self, target_decorators: Set[str] = None):
        self.target_decorators = target_decorators or {'testsuite'}
    
    def parse(self, file_path: Path) -> List[TestSuiteInfo]:
        """Parse Python file using AST to find decorated test suites."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            visitor = TestSuiteVisitor(self.target_decorators)
            visitor.visit(tree)
            
            return [
                TestSuiteInfo(
                    file_path=file_path,
                    class_name=suite['class_name'],
                    decorator_name=suite['decorator'],
                    methods=suite['methods'],
                    imports=visitor.imports
                )
                for suite in visitor.test_suites
            ]
        except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
            return []


class TestSuiteVisitor(ast.NodeVisitor):
    """AST visitor to extract test suite information."""
    
    def __init__(self, target_decorators: Set[str]):
        self.target_decorators = target_decorators
        self.test_suites = []
        self.imports = []
    
    def visit_Import(self, node):
        """Extract import statements."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        """Extract from-import statements."""
        if node.module:
            for alias in node.names:
                self.imports.append(f"{node.module}.{alias.name}")
        self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        """Visit class definitions to find decorated test suites."""
        decorators = self._extract_decorators(node)
        matching_decorators = decorators.intersection(self.target_decorators)
        
        if matching_decorators:
            methods = [method.name for method in node.body 
                      if isinstance(method, ast.FunctionDef)]
            
            self.test_suites.append({
                'class_name': node.name,
                'decorator': list(matching_decorators)[0],
                'methods': methods
            })
        
        self.generic_visit(node)
    
    def _extract_decorators(self, node) -> Set[str]:
        """Extract decorator names from a class or function node."""
        decorators = set()
        for decorator in node.decorator_list:
            if isinstance(decorator, ast.Name):
                decorators.add(decorator.id)
            elif isinstance(decorator, ast.Attribute):
                decorators.add(decorator.attr)
        return decorators