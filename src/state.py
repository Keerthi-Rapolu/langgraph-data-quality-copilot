from __future__ import annotations
from typing import Any, Dict, List, TypedDict


class DQState(TypedDict, total=False):
    # inputs
    dataset_path: str
    table_name: str
    db_path: str  

    # outputs
    profile: Dict[str, Any]
    rules: Any           
    validation: Dict[str, Any]
    report_path: str
    errors: List[str]
