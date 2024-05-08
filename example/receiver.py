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

import asyncio
import numpy as np

from shared_objects__types import *


ashared_memory_manager: ASharedMemoryManager = ASharedMemoryManager(SharedMemory('shared_objects'))


async def receiver():
    async with ashared_memory_manager as asmm:
        print('Receiver is ready.')

        # An each coroutine should get its own context manager (ASharedMemoryContextManager). Either `asmm` or `ashared_memory_manager` can be used
        ashared_memory_context_manager: ASharedMemoryContextManager = asmm()

        sso: SomeSharedObject = None  # variable for our shared object

        async with ashared_memory_context_manager.if_has_messages() as shared_memory:
            sso = shared_memory.value.take_message()  # 5_833 iterations/seconds
            company_metrics = sso.company_info.company_metrics  # 12_479 iterations/seconds
            k = company_metrics[CompanyMetrics.in_a_good_state]  # 1_154_454 iterations/seconds
            company_metrics[CompanyMetrics.in_a_good_state] = False  # 1_213_175 iterations/seconds
            company_metrics[CompanyMetrics.in_a_good_state] = None  # 1_188_630 iterations/seconds
            k = company_metrics[CompanyMetrics.employees]  # 1_498_278 iterations/seconds
            company_metrics[CompanyMetrics.employees] = 20  # 1_352_799 iterations/seconds
            company_metrics[CompanyMetrics.employees] += 1  # 247_476 iterations/seconds
            k = company_metrics[CompanyMetrics.avg_salary]  # 1_535_267 iterations/seconds
            company_metrics[CompanyMetrics.avg_salary] = 5_000.0  # 1_300_966 iterations/seconds
            company_metrics[CompanyMetrics.avg_salary] += 1.1  # 299_415 iterations/seconds
            k = sso.int_value  # 850_098 iterations/seconds
            sso.int_value = 200  # 207_480 iterations/seconds
            sso.int_value += 1  # 152_263 iterations/seconds
            company_metrics[CompanyMetrics.annual_income] = 2_000_000.0  # 1_380_983 iterations/seconds
            company_metrics[CompanyMetrics.emails] = tuple()  # 55_335 iterations/seconds
            company_metrics[CompanyMetrics.emails] = ('sails@company.com',)  # 30_314 iterations/seconds
            company_metrics[CompanyMetrics.emails] = ('sails@company.com', 'support@company.com')  # 20_860 iterations/seconds
            k = company_metrics[CompanyMetrics.websites]  # 380_258.29925590986 iterations/seconds
            company_metrics[CompanyMetrics.websites] = ['http://company.com', 'http://company.org']  # 10_465 iterations/seconds
            k = sso.str_value  # 228_966 iterations/seconds
            sso.str_value = 'Hello. '  # 52_390 iterations/seconds
            sso.str_value += '!'  # 35_823 iterations/seconds
            data_dict = sso.data_dict  # 16_362 iterations/seconds
            k = data_dict['key1']  # 87_558 iterations/seconds
            data_dict['key1'] = 200  # 86_744 iterations/seconds
            data_dict['key1'] *= 1  # 40_927 iterations/seconds
            data_dict['key1'] += 3  # 41_409 iterations/seconds
            k = data_dict[('key', 2)]  # 49_338 iterations/seconds
            data_dict[('key', 2)] = 'value2'  # 31_460 iterations/seconds
            data_dict[('key', 2)] = data_dict[('key', 2)] + 'd'  # 18_972 iterations/seconds
            data_dict[('key', 2)] = 'value2'  # 10_941 iterations/seconds
            data_dict[('key', 2)] += 'd'  # 16_568 iterations/seconds
            ndarray: np.ndarray = data_dict['key3']  # 26_223 iterations/seconds
            ndarray += 10  # 403_246 iterations/seconds
            data_dict['key3'] += 10  # 6_319 iterations/seconds
            k = sso.company_info.income  # 20_445 iterations/seconds
            sso.company_info.income = 3_000_000.0  # 13_899 iterations/seconds
            sso.company_info.income *= 1.1  # 17_272 iterations/seconds 
            sso.company_info.income += 500_000.0  # 18_376 iterations/seconds
            sso.company_info.some_employee.increase_years_of_employment()  # 9_429 iterations/seconds
            sso.some_processing_stage_control = True  # 298_968 iterations/seconds


if __name__ == '__main__':
    print('Receiver is starting its work.')
    asyncio.run(receiver())
    print('Receiver has finished its work.')
