import ast
from typing import Dict, List, Optional, TypeVar, overload

const_type = str | float | int


class Changer(ast.NodeVisitor):
    """
    A custom AST NodeVisitor that modifies assignment values in an abstract syntax tree (AST).

    This class allows replacing variable assignments based on predefined rules and
    extracting values assigned to specific variables.
    """

    rules = {}  # Dictionary containing replacement rules for variables
    extract_rules: List[str] = []  # List of variable names to extract
    extract_result: Dict[str, const_type] = {}  # Extracted variable values

    def visit_Assign(self, node: ast.Assign):
        """
        Visits assignment nodes in the AST and applies transformation rules.

        - If the target variable is in `rules`, its value is replaced with the corresponding rule value.
        - If the target variable is in `extract_rules` and is a constant, its value is stored.

        Args:
            node (ast.Assign): The assignment node being visited.
        """
        if node.targets.__len__() == 1 and isinstance(
                node.targets[0], ast.Name):
            target_id = node.targets[0].id
            if target_id in self.rules:
                node.value = ast.Constant(value=self.rules[target_id])
            if target_id in self.extract_rules and isinstance(
                    node.value, ast.Constant):
                self.extract_result.update({target_id: node.value.value})
        return self

    def add_rules(self, rules: dict[str, const_type]):
        """
        Adds variable transformation rules.

        Args:
            rules (dict[str, const_type]): A dictionary mapping variable names to new values.

        Returns:
            Changer: The updated instance of `Changer`.
        """
        self.rules.update(rules)
        return self

    def extract(self, vars_name: List[str]):
        """
        Specifies which variable values should be extracted from the AST.

        Args:
            vars_name (List[str]): List of variable names to extract.

        Returns:
            Changer: The updated instance of `Changer`.
        """
        self.extract_rules.extend(vars_name)
        return self


T = TypeVar("T", str, float, int)


class ValueChanger:
    """
    A utility class for modifying and extracting variable assignments in Python source code.

    This class parses Python source code into an AST and allows:
    - Replacing variable values.
    - Extracting assigned values from variables.
    - Converting the modified AST back to source code.
    """

    def __init__(self, source_code: str) -> None:
        """
        Initializes a `ValueChanger` instance with the provided source code.

        Args:
            source_code (str): The Python source code to be modified.
        """
        self.node = ast.parse(source_code)

    def set_value(self, name: str, value: const_type):
        """
        Replaces the assigned value of a specified variable in the source code.

        Args:
            name (str): The name of the variable to modify.
            value (const_type): The new value to assign.

        Returns:
            ValueChanger: The updated instance of `ValueChanger`.
        """
        Changer().add_rules({name: value}).visit(self.node)
        return self

    @overload
    def extract(self, name: str, expect_type: type[T]) -> T: ...
    @overload
    def extract(self, name: str) -> const_type: ...

    def extract(self, name: str,
                expect_type: Optional[type[const_type]] = None) -> const_type:
        """
        Extracts the assigned value of a specified variable from the source code.

        Args:
            name (str): The variable name to extract.
            expect_type (Optional[type[const_type]]): The expected type of the extracted value (optional).

        Returns:
            const_type: The extracted value of the variable.
        """
        changer = Changer()
        changer.extract([name]).visit(self.node)
        return changer.extract_result[name]

    def extracts(self, names: List[str]) -> Dict[str, const_type]:
        """
        Extracts assigned values for multiple variables from the source code.

        Args:
            names (List[str]): List of variable names to extract.

        Returns:
            Dict[str, const_type]: A dictionary mapping variable names to their extracted values.
        """
        changer = Changer()
        changer.extract(names).visit(self.node)
        return changer.extract_result

    @property
    def text(self) -> str:
        """
        Returns the modified source code as a string after applying transformations.

        Returns:
            str: The transformed source code.
        """
        return ast.unparse(self.node)


if __name__ == "__main__":
    print(ValueChanger("x = 3\nd= 5").set_value("d", 100).text)
