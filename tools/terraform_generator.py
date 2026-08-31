import re
import os
from typing import Tuple

class TerraformGenerator:
    """
    Parses, validates, and modifies Terraform HCL code for right-sizing changes.
    """
    @staticmethod
    def update_node_count(file_path: str, old_count: int, new_count: int) -> Tuple[bool, str, str]:
        """
        Updates node_count in target Terraform file.
        Returns (success, original_content, updated_content)
        """
        if not os.path.exists(file_path):
            return False, "", ""

        with open(file_path, "r") as f:
            original_content = f.read()

        # Regex matching node_count = <old_count> or node_count\s*=\s*\d+
        pattern = r"(node_count\s*=\s*)" + str(old_count)
        replacement = r"\g<1>" + str(new_count)

        if re.search(pattern, original_content):
            updated_content = re.sub(pattern, replacement, original_content)
            return True, original_content, updated_content
        else:
            # Fallback pattern for node_count
            pattern_any = r"(node_count\s*=\s*)\d+"
            if re.search(pattern_any, original_content):
                updated_content = re.sub(pattern_any, r"\g<1>" + str(new_count), original_content)
                return True, original_content, updated_content

        return False, original_content, original_content

    @staticmethod
    def write_patch(file_path: str, updated_content: str) -> bool:
        try:
            with open(file_path, "w") as f:
                f.write(updated_content)
            return True
        except Exception:
            return False
