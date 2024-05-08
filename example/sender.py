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


from ipc_py_objects import *

# An alternative imports:
# from cengal.hardware.memory.shared_memory import *
# from cengal.parallel_execution.asyncio.ashared_memory_manager import *

import numpy as np

import asyncio

from shared_objects__types import *


ashared_memory_manager: ASharedMemoryManager = ASharedMemoryManager(SharedMemory('shared_objects', True, 200 * 1024**2))


def printval(name, value):
    print(f'> {name}:\n\t{value}\n')


def printtitle(name):
    title_str: str = f'<<< {name}: >>>'
    header_str: str = '=' * len(title_str)
    print(header_str)
    print(title_str)
    print(header_str)
    print()


async def sender():
    sso: SomeSharedObject = SomeSharedObject(
        some_processing_stage_control=False,
        int_value=18,
        str_value='Hello, ',
        data_dict={
            'key1': 1,
            ('key', 2): 'value2',
            'key3': np.array([1, 2, 3], dtype=np.int32),
        },
        company_info=CompanyInfo(
            company_id=1,
            emails=('sails@company.com', 'support@company.com'),
            websites=['http://company.com', 'http://company.org'],
            income=1_000_000.0,
            employees=10,
            some_employee=Employee(
                'John Doe', 
                30, 
                Positions.manager,
                2,
            ),
            company_metrics=intenum_dict_to_list({  # lists with IntEnum indexes are blazing-fast alternative to dictionaries
                CompanyMetrics.websites: ['http://company.com', 'http://company.org'],
                CompanyMetrics.avg_salary: 3_000.0,
                CompanyMetrics.employees: 10,
                CompanyMetrics.in_a_good_state: True,
            })  # Unmentioned fields will be filled with Null values
        )
    )

    async with ashared_memory_manager as asmm:
        print('Sender is ready.')

        # An each coroutine should get its own context manager (ASharedMemoryContextManager). Either `asmm` or `ashared_memory_manager` can be used
        ashared_memory_context_manager: ASharedMemoryContextManager = asmm()

        async with ashared_memory_context_manager as shared_memory:
            sso_mapped: SomeSharedObject = shared_memory.value.put_message(sso)  # by default, for custom classes including dataclass, `sso` is `sso_mapped`
        
        while True:
            async with ashared_memory_context_manager as shared_memory:
                shared_memory.existence = False  # This coroutine allows small sleep time for current loop before next iteration with shared memory
                if sso.some_processing_stage_control:
                    break
        
        # The receiver has finished processing. The shared object has been changed. Let's see what has been changed
        printtitle('Fields expeced to be changed by the receiver')
        printval('sso.some_processing_stage_control', sso.some_processing_stage_control)
        printval('sso.int_value', sso.int_value)
        printval('sso.str_value', sso.str_value)
        printval('sso.data_dict', sso.data_dict)
        printval('sso.company_info.income', sso.company_info.income)
        printval('sso.company_info.some_employee.years_of_employment', sso.company_info.some_employee.years_of_employment)
        printval('sso.company_info.some_employee.age', sso.company_info.some_employee.age)
        printval('sso.company_info.company_metrics[CompanyMetrics.annual_income]', sso.company_info.company_metrics[CompanyMetrics.annual_income])
        printval('sso.company_info.company_metrics[CompanyMetrics.emails]', sso.company_info.company_metrics[CompanyMetrics.emails])
        printval('sso.company_info.company_metrics[CompanyMetrics.websites]', sso.company_info.company_metrics[CompanyMetrics.websites])
        printval('sso.company_info.company_metrics[CompanyMetrics.avg_salary]', sso.company_info.company_metrics[CompanyMetrics.avg_salary])
        printval('sso.company_info.company_metrics[CompanyMetrics.employees]', sso.company_info.company_metrics[CompanyMetrics.employees])
        printval('sso.company_info.company_metrics[CompanyMetrics.in_a_good_state]', sso.company_info.company_metrics[CompanyMetrics.in_a_good_state])

        printtitle('Resulting content')
        printval('sso', sso)
        printval('sso.company_info', sso.company_info)
        printval('sso.company_info.some_employee', sso.company_info.some_employee)

if __name__ == '__main__':
    print('Sender is starting its work.')
    asyncio.run(sender())
    print('Sender has finished its work.')
