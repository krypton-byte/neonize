import ast
from typing import Dict, List, Optional, TypeVar, overload

const_type = str | float | int

class Changer(ast.NodeVisitor):
    rules = {}
    extract_rules: List[str] = []
    extract_result: Dict[str, const_type] = {}
    def visit_Assign(self, node: ast.Assign):
        if node.targets.__len__() == 1 and isinstance(node.targets[0], ast.Name):
            target_id = node.targets[0].id
            if target_id in self.rules:
                node.value = ast.Constant(value=self.rules[target_id])
            elif target_id in self.extract_rules and isinstance(node.value, ast.Constant):
                self.extract_result.update({target_id: node.value.value})
        
    def add_rules(self, rules: dict[str, const_type]):
        self.rules.update(rules)
        return self

    def extract(self, vars_name: List[str]):
        self.extract_rules.extend(vars_name)
        return self

T = TypeVar('T', str, float, int)

class ValueChanger:
    def __init__(self, source_code: str) -> None:
        self.node = ast.parse(source_code)
    def set_value(self, name: str, value: const_type):
        Changer().add_rules({name: value}).visit(self.node)
        return self
    @overload
    def extract(self, name: str, expect_type: type[T]) -> T: ...
    @overload
    def extract(self, name: str) -> const_type: ...

    def extract(self, name: str, expect_type: Optional[type[const_type]] = None) -> const_type:
        changer = Changer()
        changer.extract([name]).visit(self.node)
        return changer.extract_result[name]
    def extracts(self, names: List[str]) -> Dict[str, const_type]:
        changer = Changer()
        changer.extract(names).visit(self.node)
        return changer.extract_result
    @property
    def text(self):
        return ast.unparse(self.node)

if __name__ == '__main__':
    print(ValueChanger("x = 3\nd= 5").set_value('d', 100).text)