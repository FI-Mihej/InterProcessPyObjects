#!/usr/bin/env python
# coding=utf-8

# Copyright © 2012-2024 ButenkoMS. All rights reserved. Contacts: <gtalk@butenkoms.space>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


__all__ = [
    'Positions',
    'Employee',
    'CompanyMetrics',
    'CompanyInfo',
    'SomeSharedObject',
]


"""
Module Docstring
Docstrings: http://www.python.org/dev/peps/pep-0257/
"""

__author__ = "ButenkoMS <gtalk@butenkoms.space>"
__copyright__ = "Copyright © 2012-2024 ButenkoMS. All rights reserved. Contacts: <gtalk@butenkoms.space>"
__credits__ = ["ButenkoMS <gtalk@butenkoms.space>", ]
__license__ = "Apache License, Version 2.0"
__version__ = "4.4.0"
__maintainer__ = "ButenkoMS <gtalk@butenkoms.space>"
__email__ = "gtalk@butenkoms.space"
# __status__ = "Prototype"
__status__ = "Development"
# __status__ = "Production"


from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Tuple, List, Dict, Hashable, Union


class Positions(IntEnum):
    manager = 0
    designer = 1
    accountant = 2
    lawyer = 3


class Employee:
    def __init__(self, name: str, age: int, position: Positions, years_of_employment: int = 0):
        self.name = name
        self.age = age
        self.position = position
        self.years_of_employment = years_of_employment
    
    def increase_years_of_employment(self):
        self.years_of_employment += 1
        self.age += 1
    
    def __repr__(self):
        return f'Employee(name={self.name}, age={self.age}, position={self.position}, years_of_employment={self.years_of_employment})'
    
    def __str__(self):
        return self.__repr__()


class CompanyMetrics(IntEnum):
    income = 0
    employees = 1
    avg_salary = 2
    annual_income = 3
    in_a_good_state = 4
    emails = 5
    websites = 6


@dataclass
class CompanyInfo:
    company_id: int
    emails: Tuple[str, str]
    websites: List[str]
    income: float
    employees: int
    some_employee: Employee
    company_metrics: List


@dataclass
class SomeSharedObject:
    some_processing_stage_control: bool
    int_value: int
    str_value: str
    data_dict: Dict[Hashable, Any]
    company_info: CompanyInfo
