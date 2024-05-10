![GitHub tag (with filter)](https://img.shields.io/github/v/tag/FI-Mihej/InterProcessPyObjects) ![Static Badge](https://img.shields.io/badge/OS-Linux_%7C_Windows_%7C_macOS-blue)

![PyPI - Version](https://img.shields.io/pypi/v/InterProcessPyObjects) ![PyPI - Format](https://img.shields.io/pypi/format/cengal-light?color=darkgreen) ![Static Badge](https://img.shields.io/badge/wheels-Linux_%7C_Windows_%7C_macOS-blue) ![Static Badge](https://img.shields.io/badge/Architecture-x86__64_%7C_ARM__64-blue) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cengal-light) ![Static Badge](https://img.shields.io/badge/PyPy-3.8_%7C_3.9_%7C_3.10-blue) ![PyPI - Implementation](https://img.shields.io/pypi/implementation/cengal-light) 

![GitHub License](https://img.shields.io/github/license/FI-Mihej/InterProcessPyObjects?color=darkgreen) ![Static Badge](https://img.shields.io/badge/API_status-Stable-darkgreen)

# InterProcessPyObjects package

This high-performance package delivers blazing-fast inter-process communication through shared memory, enabling Python objects to be shared across processes with exceptional efficiency. By minimizing the need for frequent serialization-deserialization, it enhances overall speed and responsiveness. The package offers a comprehensive suite of functionalities designed to support a diverse array of Python types and facilitate asynchronous IPC, optimizing performance for demanding applications.

![title](https://github.com/FI-Mihej/Cengal/raw/master/docs/assets/InterProcessPyObjects/ChartThroughputGiBs.png)

## API State

Stable. Guaranteed to not have braking changes in the future (see bellow for details).

Any hypothetical further API-breaking changes will lead to new module creation within the package. An old version will continue its existence and continue to be importable by an explicit address (see Details bellow).

<details>
<summary title="Details"><kbd> Details </kbd></summary>

The current (currently latest) version can be imported either by:

```python
from ipc_py_objects import *
```

or by

```python
from ipc_py_objects.versions.v_1 import *
```

If further braking changes will be made to the API - a new (`v_2`) version will be made. As result:

Current (`v_1`) version will continue to be accessible by an explicit address:

```python
from ipc_py_objects.versions.v_1 import *
```

Latest (`v_2`) version will be accessible by either: 

```python
from ipc_py_objects import *
```

or by

```python
from ipc_py_objects.versions.v_2 import *
```

This is a general approach across the entire [Cengal](https://github.com/FI-Mihej/Cengal) library. It gives me the ability to effectively work on its huge codebase, even by myself.

By the way. I'm finishing an implementation of [CengalPolyBuild](https://github.com/FI-Mihej/CengalPolyBuild) - my package creation system which provides same approach to users. It is a comprehensive and hackable build system for multilingual Python packages: Cython (including automatic conversion from Python to Cython), C/C++, Objective-C, Go, and Nim, with ongoing expansions to include additional languages. Basically, it will provide easy access to all the same features I'm already using in the Cengal library package creation and management processes.

</details>

## Key Features

* Shared Memory Communication:
    * Enables sharing of Python objects directly between processes using shared memory.
    * Utilizes a linked list of global messages to inform connected processes about new shared objects.

* Lock-Free Synchronization:
    * Uses memory barriers for efficient communication, avoiding slow syscalls.
    * Ensures each process can access and modify shared memory without contention.

* Supported Python Types:
    * Handles various Python data structures including:
        * Basic types: `None`, `bool`, 64-bit `int`, large `int` (arbitrary precision integers), `float`, `complex`, `bytes`, `bytearray`, `str`.
        * Standard types: `Decimal`, `slice`, `datetime`, `timedelta`, `timezone`, `date`, `time`
        * Containers: `tuple`, `list`, classes inherited from: `AbstractSet` (`frozenset`), `MutableSet` (`set`), `Mapping` and `MutableMapping` (`dict`).
        * Pickable classes instancess: custom classes including `dataclass`
    * Allows mutable containers (lists, sets, mappings) to save basic types (`None`, `bool`, 64 bit `int`, `float`) internally, optimizing memory use and speed.

* NumPy and Torch Support:
    * Supports numpy arrays by creating shared bytes objects coupled with independent arrays.
    * Supports torch tensors by coupling them with shared numpy arrays.

* Custom Class Support:
    * Projects pickable custom classes instancess (including `dataclasses`) onto shared dictionaries in shared memory.
    * Modifies the class instance to override attribute access methods, managing data fields within the shared dictionary.
    * supports classes with or without `__dict__` attr
    * supports classes with or without `__slots__` attr

* Asyncio Compatibility:
    * Provides a wrapper module for async-await functionality, integrating seamlessly with asyncio.
    * Ensures asynchronous operations work smoothly with the package's lock-free approach.

## Import

To use this package, simply install it via pip:

```shell
pip install InterProcessPyObjects
```

Then import it into your project:

```python
from ipc_py_objects import *
```

## Main principles

* only one process has access to the shared memory at the same time
* working cycle:
    1. work on your tasks
    2. acacquire access to shared memory
    3. work with shared memory as fast as possible (read and/or update data structures in shared memory)
    4. release access to shared memory
    5. continue your work on other tasks
* do not forget to manually destroy your shared objects when they are not needed already
* feel free to not destroy your shared object if you need it for a whole run and/or do not care about the shared memory waste
* data will not be preserved between Creator's sessions. Shared memory will be wiped just before Creator finished its work with a shared memory instance (Consumer's session will be finished already at this point)

### ! Important about hashmaps

Package, currently, uses Python `hash()` call which is reliable across interpreter session but unreliable across different interpreter sessions because of random seeding.

In order to use same seeding across different interpeter instancess (and as result, be able to use hashmaps) you can set 'PYTHONHASHSEED` env var to some fixed integer value

<details>
<summary title=".bashrc"><kbd> .bashrc </kbd></summary>

```bash
export PYTHONHASHSEED=0
```

</details>

<details>
<summary title="Your bash script"><kbd> Your bash script </kbd></summary>

```bash
export PYTHONHASHSEED=0
python YOURSCRIPT.py
```

</details>

<details>
<summary title="Terminal"><kbd> Terminal </kbd></summary>

```shell
$ PYTHONHASHSEED=0 python YOURSCRIPT.py
```

</details>

An issue with the behavior of an integrated `hash()` call **does Not** affect the following data types:
* `None`, `bool`, `int`, `float`, `complex`, `str`, `bytes`, `bytearray`
* `Decimal`, `slice`, `datetime`, `timedelta`, `timezone`, `date`, `time`
* `tuple`, `list`
* `set` wrapped by `FastLimitedSet` class instance: for example by using `.put_message(FastLimitedSet(my_set_obj))` call
* `dict` wrapped by `FastLimitedDict` class instance: for example by using `.put_message(FastLimitedDict(my_dict_obj))` call
* an instancess of custom classes including `dataclass` by default: for example by using `.put_message(my_obj)` call
* an instancess of custom classes including `dataclass` wrapped by `ForceStaticObjectCopy` or `ForceStaticObjectInplace` class instancess. For example by using `.put_message(ForceStaticObjectInplace(my_obj))` call

It affects only the following data types: 
* `AbstractSet` (`frozenset`)
* `MutableSet` (`set`)
* `Mapping`
* `MutableMapping` (`dict`)
* an instancess of custom classes including `dataclass` wrapped by `ForceGeneralObjectCopy` or `ForceGeneralObjectInplace` class instancess. For example by using `.put_message(ForceGeneralObjectInplace(my_obj))` call

## Examples

* An async examples (with asyncio):
    * [sender.py](https://github.com/FI-Mihej/InterProcessPyObjects/blob/master/example/sender.py)
    * [receiver.py](https://github.com/FI-Mihej/InterProcessPyObjects/blob/master/example/receiver.py)
    * [shared_objects__types.py](https://github.com/FI-Mihej/InterProcessPyObjects/blob/master/example/shared_objects__types.py)

### Receiver.py performance measurements

```python
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
    k = company_metrics[CompanyMetrics.websites]  # 380_258 iterations/seconds
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
```

## Reference (and explaining examples line by line)

Code for shared memory Creator side:
```python
ashared_memory_manager: ASharedMemoryManager = ASharedMemoryManager(SharedMemory('shared_memory_identifier', create=True, size=200 * 1024**2))
# declare creation and initiation of the shared memory instance with a size of 200 MiB.
```

Code for shared memory Consumer side:
```python
ashared_memory_manager: ASharedMemoryManager = ASharedMemoryManager(SharedMemory('shared_memory_identifier'))
# declares connection to shared memory instance
```

On shared memory Creator side:
```python
async with ashared_memory_manager as asmm:
# creates, initiates shared memory instance and waits for the Consumer creation. Execute it once per run.
# feel free to share either `asmm` or `ashared_memory_manager` across your coroutines
```

On shared memory concumer side:
```python
async with ashared_memory_manager as asmm:
# waits for the shared memory creation and initiation by the shared memory Creator. Execute it once per run.
# feel free to share either `asmm` or `ashared_memory_manager` across your coroutines
```

```python
ashared_memory_context_manager: ASharedMemoryContextManager = asmm()
# creates shared memory access context manager. Create it once per coroutine. Use in the same coroutine as much as you need it.
```

```python
async with ashared_memory_context_manager as shared_memory:
# acacquire access to shared memory as soon as possible
```

```python
async with ashared_memory_context_manager.if_has_messages() as shared_memory:
# acacquire access to shared memory if message queue is not empty
```

```python
shared_memory # is an instance of ValueHolder class from the Cengal library
shared_memory.value  # is an instance of `SharedMemory` instance
shared_memory.existence  # bool. Will be set to True at the beginning of an eash context (`with`) block. Set it to `False`
    # if you want to release CPU for a small time portion before shared memory will be acacquired next time.
    # if at least one coroutine will not set it to `False` - next acacquire attempt will be made immidiately which will
    # lower latency and increase performance but at the same time will consume more CPU time.
    # Default behavior (`True`) is better for CPU intensive algorithms, 
    # while `False` on all process coroutines (which have their own memory access context managers) will be better
    # for example for desktop or mobile applications
```

### `SharedMemory` fields and methods you might frequently use in an async approach (in coroutines)

```python
SharedMemory.size  # an actual size of the shared memory
```

```python
SharedMemory.name  # an identifier of the shared memory
```

```python
SharedMemory.create  # `True` on Creator side. `False` on Consumer side
```

```python
obj_mapped = shared_memory.value.put_message(obj)
# Puts object to the shared memory and create an appropriate message
# Returns mapped version of the object if applicable (returns the same object otherwise).
# Next types will return same object: None, bool, int, float, str, bytes, bytearray, tuple.
```

```python
obj_mapped, shared_obj_offset = shared_memory.value.put_message_2(obj)
# Puts object to the shared memory and create an appropriate message
# Returns: 
# * Mapped version of the object if applicable (returns the same object otherwise).
#   Next types will return same object: None, bool, int, float, str, bytes, bytearray, tuple.
# * An offset to the shared object data structure which holds an appropriate shared object content
```

```python
has_messages: bool = shared_memory.value.has_messages()
# main way for checking an internal message queue for an emptiness
```

```python
obj_mapped = shared_memory.value.take_message()
# Takes (and removes) the latest message from an internal message queue.
# Creates and returns mapped object from an appropriate shared object data structure.
# Does not deletes an appropriate shared object data structure.
# Returns mapped version of the object if applicable (returns new copy of an object otherwise).
# Next types will return new copy of an object: None, bool, int, float, str, bytes, bytearray, tuple.
# Will raise NoMessagesInQueueError exception if an internal message queue is empty
```

```python
obj_mapped, shared_obj_offset = shared_memory.value.take_message_2()
# Takes (and removes) the latest message from an internal message queue.
# Creates and returns mapped object from an appropriate shared object data structure.
# Does not deletes an appropriate shared object data structure.
# Returns: 
# * Mapped version of the object if applicable (returns new copy of an object otherwise).
#   Next types will return new copy of an object: None, bool, int, float, str, bytes, bytearray, tuple.
# * An offset to the shared object data structure which holds an appropriate shared object content
# Will raise NoMessagesInQueueError exception if an internal message queue is empty
```

```python
shared_memory.value.destroy_obj(shared_obj_offset)
# Destroys the shared object data structure which holds an appropriate shared object content.
# Use it in order to free memory used by your shared object.


shared_memory.value.destroy_object(shared_obj_offset)
# An alias to the `shared_memory.value.destroy_obj()` call
```

```python
shared_obj_buffer: memoryview = shared_memory.value.get_obj_buffer(shared_obj_offset)
# returns `memoryview` to the data section of your shared object.
# Feel free to use this memory for your own needs while an appropriate shared object is still not destroyed.
# Next types provides buffer to their shared data: bytes, bytearray, str, numpy.ndarray (buffer of an appropriate shared bytes object mapped by this ndarray), torch.Tensor (buffer of an appropriate shared bytes object mapped by this Tensor)
```

### Useful exceptions

```python
class SharedMemoryError:
# Base exception all other exceptions are inherited from it
```

```python
class FreeMemoryChunkNotFoundError(SharedMemoryError):
"""Indicates that an unpartitioned chunk of free memory of requested size not being found.

    Regarding this error, it’s important to adjust the size parameter in the SharedMemory configuration. Trying to estimate memory consumption down to the byte is not practical because it fails to account for the memory overhead required by each entity stored (such as entity type metadata, pointers to child entities, etc.).

    When setting the size parameter for SharedMemory, consider using broader units like tens (for embedded systems), hundreds, or thousands of megabytes, rather than precise byte counts. This approach is similar to how you would not precisely calculate the amount of memory needed for a web server hosted externally; you make an educated guess, like assuming that 256 MB might be insufficient but 768 MB could be adequate, and then adjust based on practical testing.

    Also, be aware of memory fragmentation, which affects all memory allocation systems, including the OS itself. For example, if you have a SharedMemory pool sized to store exactly ten 64-bit integers, accounting for additional bytes for system information, your total might be around 200 bytes. Initially, after storing the integers, your memory might appear as ["int", "int", ..., "int"]. If you delete every second integer, the largest contiguous free memory chunk could be just 10 bytes, despite having 50 bytes free in total. This fragmentation means you cannot store a larger data structure like a 20-byte string which needs contiguous space.

    To resolve this, simply increase the size parameter value of SharedMemory. This is akin to how you would manage memory allocation for server hosting or thread stack sizes in software development.
"""
```

```python
NoMessagesInQueueError
# Next calls can raise it if an internal message queue is empty: take_message(), take_message_2(), read_message(), read_message_2()
```

## Performance tips

<details>
<summary title="Data structures"><kbd> Data structures </kbd></summary>

### Data structures

It is recommended to use `IntEnum`+`list` based data structures instead of dictionaries or even instead custom class instancess (including dataclass) if you want best performance.

For example instead operating with dict:

<details>
<summary title="Example"><kbd> Example </kbd></summary>

Message sender

```python
company_metrics: Dict[str, Any] = {
    'websites': ['http://company.com', 'http://company.org'],
    'avg_salary': 3_000.0,
    'employees': 10,
    'in_a_good_state': True,
}
company_metrics_mapped: List = shared_memory.value.put_message(company_metrics)
```

Message receiver

```python
company_metrics: Dict[str, Any] = shared_memory.value.take_message()
k = company_metrics['employees']  # 87_558 iterations/seconds
company_metrics['employees'] = 200  # 86_744 iterations/seconds
company_metrics['employees'] += 3  # 41_409 iterations/seconds
```

</details>
<br>

or even instead operating with dataclass (classess by default operate faster then dict):

<details>
<summary title="Example"><kbd> Example </kbd></summary>

Message sender

```python
@dataclass
class CompanyMetrics:
    income: float
    employees: int
    avg_salary: float
    annual_income: float
    in_a_good_state: bool
    emails: Tuple
    websites = List[str]

company_metrics: CompanyMetrics = CompanyMetrics(
    income=1.4,
    employees: 12,
    avg_salary: 35.0,
    annual_income: 30_000.0,
    in_a_good_state: False,
    emails: ('sails@company.com', 'support@company.com'),
    websites = ['http://company.com', 'http://company.org'],
)
company_metrics_mapped: CompanyMetrics = shared_memory.value.put_message(company_metrics)
```

Message receiver

```python
company_metrics: CompanyMetrics = shared_memory.value.take_message()
k = company_metrics.employees  # 850_098 iterations/seconds
company_metrics.employees = 200  # 207_480 iterations/seconds
company_metrics.employees += 1  # 152_263 iterations/seconds
```

</details>
<br>

it would be more beneficial to operate with a list and appropriate IntEnum indexes:

<details>
<summary title="Example"><kbd> Example </kbd></summary>

Message sender:

```python
class CompanyMetrics(IntEnum):
    income = 0
    employees = 1
    avg_salary = 2
    annual_income = 3
    in_a_good_state = 4
    emails = 5
    websites = 6

company_metrics: List = intenum_dict_to_list({  # lists with IntEnum indexes are blazing-fast alternative to dictionaries
    CompanyMetrics.websites: ['http://company.com', 'http://company.org'],
    CompanyMetrics.avg_salary: 3_000.0,
    CompanyMetrics.employees: 10,
    CompanyMetrics.in_a_good_state: True,
})  # Unmentioned fields will be filled with Null values
company_metrics_mapped: List = shared_memory.value.put_message(company_metrics)
```

Message receiver:

```python
company_metrics: List = shared_memory.value.take_message()
k = company_metrics[CompanyMetrics.avg_salary]  # 1_535_267 iterations/seconds
company_metrics[CompanyMetrics.avg_salary] = 5_000.0  # 1_300_966 iterations/seconds
company_metrics[CompanyMetrics.avg_salary] += 1.1  # 299_415 iterations/seconds
```

</details>
<br>

</details>

<details>
<summary title="Sets"><kbd> Sets </kbd></summary>

### Sets

You might use `FastLimitedSet` wrapper for your set in order to get much faster shared sets.

Just wrap your dictionary with `FastLimitedSet`:

```python
my_obj: List = [
    True,
    2,
    FastLimitedSet({
        'Hello ',
        'World',
        3,
    })
]
my_obj_mapped = shared_memory.value.put_message(my_obj)
```

Drawbacks of this approach: only initial set of items will be shared. Changes made to the mapped objects (an added or deleted items) will not be shared and will not be visible by other process.

</details>

<details>
<summary title="Dictionaries"><kbd> Dictionaries </kbd></summary>

### Dictionaries

You might use `FastLimitedDict` wrapper for your dict in order to get much faster shared dictionary.

Just wrap your dictionary with `FastLimitedDict`:

```python
my_obj: List = [
    True,
    2,
    FastLimitedDict({
        1: 'Hello ',
        '2': 'World',
        3: np.array([1, 2, 3], dtype=np.int32),
    })
]
my_obj_mapped = shared_memory.value.put_message(my_obj)
```

Drawbacks of this approach: only initial set of key-values pairs will be shared. Added, updated or deleted key-value pairs will not be shared and such changes will not be visible by other process.

</details>

<details>
<summary title="Custom classes (including `dataclass`)"><kbd> Custom classes (including `dataclass`) </kbd></summary>

### Custom classes (including `dataclass`)

By default, shared custom class instancess (including `dataclass` instancess) have static set of attributes (similar to instancess of classes with `__slots__`). That means that all new (dynamically added to the mapped object, attributes will not became shared). This behavior increases performance.

<details>
<summary title="For example"><kbd> For example </kbd></summary>

#### For example

```python
@dataclass
class SomeSharedObject:
    some_processing_stage_control: bool
    int_value: int
    str_value: str
    data_dict: Dict[Hashable, Any]
    company_info: CompanyInfo

my_obj: List = [
    True,
    2,
    SomeSharedObject(
        some_processing_stage_control=False,
        int_value=18,
        str_value='Hello, ',
        data_dict=None,
        company_info=None,
    ),
]
my_obj_mapped: List = shared_memory.value.put_message(my_obj)

my_obj_mapped[2].some_new_attribute = 'Hi!'  # this attribute will Not became shared and as result will not became accessible by other process
```

</details>

If you need to share class instance with ability to add new shared attributes to it's mapped instance, you can wrap your object with either `ForceGeneralObjectCopy` or `ForceGeneralObjectInplace`

<details>
<summary title="For example"><kbd> For example </kbd></summary>

#### For example

```python
@dataclass
class SomeSharedObject:
    some_processing_stage_control: bool
    int_value: int
    str_value: str
    data_dict: Dict[Hashable, Any]
    company_info: CompanyInfo

my_obj: List = [
    True,
    2,
    ForceGeneralObjectInplace(SomeSharedObject(
        some_processing_stage_control=False,
        int_value=18,
        str_value='Hello, ',
        data_dict=None,
        company_info=None,
    )),
]
my_obj_mapped: List = shared_memory.value.put_message(my_obj)

my_obj_mapped[2].some_new_attribute = 'Hi!'  # this attribute Will became shared and as result Will be seen by process
```

</details>

Difference between `ForceGeneralObjectCopy` and `ForceGeneralObjectInplace`:
* `ForceGeneralObjectInplace`. `my_obj_mapped = shared_memory.value.put_message(ForceGeneralObjectInplace(my_obj))` call will change class of an original `my_obj` object. And `True == (my_obj is my_obj_mapped)`
* `ForceGeneralObjectCopy`. `my_obj_mapped = shared_memory.value.put_message(ForceGeneralObjectCopy(my_obj))` call will Not change an original `my_obj` object. `my_obj_mapped` object will be constructed from the scratch

Also you can tune a default behavior by wrapping your object with either `ForceStaticObjectCopy` or `ForceStaticObjectInplace`.

Difference between `ForceStaticObjectCopy` and `ForceGeneralObjectInplace`:
* `ForceGeneralObjectInplace`. `my_obj_mapped = shared_memory.value.put_message(ForceGeneralObjectInplace(my_obj))` call will change class of an original `my_obj` object. And `True == (my_obj is my_obj_mapped)`
* `ForceStaticObjectCopy`. `my_obj_mapped = shared_memory.value.put_message(ForceStaticObjectCopy(my_obj))` call will Not change an original `my_obj` object. `my_obj_mapped` object will be constructed from the scratch

</details>

## How to choose shared memory size

<details>
<summary title="How to choose shared memory size"><kbd> How to choose shared memory size </kbd></summary>

When setting the size parameter for SharedMemory, consider using broader units like tens (for embedded systems), hundreds, or thousands of megabytes, rather than precise byte counts. This approach is similar to how you would not precisely calculate the amount of memory needed for a web server hosted externally; you make an educated guess, like assuming that 256 MB might be insufficient but 768 MB could be adequate, and then adjust based on practical testing.

Also, be aware of memory fragmentation, which affects all memory allocation systems, including the OS itself. For example, if you have a SharedMemory pool sized to store exactly ten 64-bit integers, accounting for additional bytes for system information, your total might be around 200 bytes. Initially, after storing the integers, your memory might appear as ["int", "int", ..., "int"]. If you delete every second integer, the largest contiguous free memory chunk could be just 10 bytes, despite having 50 bytes free in total. This fragmentation means you cannot store a larger data structure like a 20-byte string which needs contiguous space.

To resolve this, simply increase the size parameter value of SharedMemory. This is akin to how you would manage memory allocation for server hosting or thread stack sizes in software development.

</details>

## Benchmarks

<details>
<summary title="System"><kbd> System </kbd></summary>

* CPU: i5-3570@3.40GHz (Ivy Bridge)
* RAM: 32 GBytes, DDR3, dual channel, 655 MHz
* OS: Ubuntu 20.04.6 LTS under WSL2. Windows 10

</details>

### Throughput GiB/s

#### Refference results (sysbench)

```bash
sysbench memory --memory-oper=write run
```

```
5499.28 MiB/sec
```

#### Results

![title](https://github.com/FI-Mihej/Cengal/raw/master/docs/assets/InterProcessPyObjects/ChartThroughputGiBs.png)

`*` [multiprocessing.shared_memory.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__shared_memory.py) - simple implementation. This is a simple implementation because it uses a similar approach to the one used in `uvloop.*`, `asyncio.*`, `multiprocessing.Queue`, and `multiprocessing.Pipe` benchmarking scripts. Similar implementations are expected to be used by the majority of projects.

<details>
<summary title="Benchmarks results table"><kbd> Benchmarks results table </kbd></summary>

#### Benchmarks results table

| Approach                        | sync/async | Throughput GiB/s |
|---------------------------------|------------|------------------|
| InterProcessPyObjects (sync)    | sync       | 3.770            |
| InterProcessPyObjects + uvloop  | async      | 3.222            |
| InterProcessPyObjects + asyncio | async      | 3.079            |
| multiprocessing.shared_memory   | sync       | 2.685            |
| uvloop.UnixDomainSockets        | async      | 0.966            |
| asyncio + cengal.Streams        | async      | 0.942            |
| uvloop.Streams                  | async      | 0.922            |
| asyncio.Streams                 | async      | 0.784            |
| asyncio.UnixDomainSockets       | async      | 0.708            |
| multiprocessing.Queue           | sync       | 0.669            |
| multiprocessing.Pipe            | sync       | 0.469            |

</details>


<details>
<summary title="Benchmark scripts"><kbd> Benchmark scripts </kbd></summary>

#### Benchmark scripts

* InterProcessPyObjects - Sync:
    * [sender.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_sync__sender.py)
    * [receiver.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_sync__receiver.py)
* InterProcessPyObjects - Async (uvloop):
    * [sender.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_uvloop__sender.py)
    * [receiver.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_uvloop__receiver.py)
* InterProcessPyObjects - Async (asyncio):
    * [sender.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_asyncio__sender.py)
    * [receiver.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/shared_objects__transfer_asyncio__receiver.py)
* [multiprocessing.shared_memory.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__shared_memory.py)
* [uvloop.UnixDomainSockets.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__uvloop_unix_domain_sockets.py)
* [asyncio_with_cengal.Streams.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__cengal_efficient_streams.py)
* [uvloop.Streams.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__uvloop_streams.py)
* [asyncio.Streams.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__asyncio_streams.py)
* [asyncio.UnixDomainSockets.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__asyncio_unix_domain_sockets.py)
* [multiprocessing.Queue.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__multiprocess_queue.py)
* [multiprocessing.Pipe.py](https://github.com/FI-Mihej/Cengal/blob/master/cengal/parallel_execution/asyncio/ashared_memory_manager/versions/v_0/development/plain_python__send_bytes__multiprocess_pipe.py)

</details>

## Todo

- [ ] Connect more than two processes
- [ ] Use third-party fast hashing implementations instead of or in addition to built in `hash()` call
- [ ] Continuous performance improvements

## Conclusion

This Python package provides a robust solution for interprocess communication, supporting a variety of Python data structures, types, and third-party libraries. Its lock-free synchronization and asyncio compatibility make it an ideal choice for high-performance, concurrent execution.

# Based on [Cengal](https://github.com/FI-Mihej/Cengal)

This is a stand-alone package for a specific Cengal module. Package is designed to offer users the ability to install specific Cengal functionality without the burden of the library's full set of dependencies.

The core of this approach lies in our 'cengal-light' package, which houses both Python and compiled Cengal modules. The 'cengal' package itself serves as a lightweight shell, devoid of its own modules, but dependent on 'cengal-light[full]' for a complete Cengal library installation with all required dependencies.

An equivalent import:
```python
from cengal.hardware.memory.shared_memory import *
from cengal.parallel_execution.asyncio.ashared_memory_manager import *
```

Cengal library can be installed by:

```bash
pip install cengal
```

https://github.com/FI-Mihej/Cengal

https://pypi.org/project/cengal/


# Projects using Cengal

* [CengalPolyBuild](https://github.com/FI-Mihej/CengalPolyBuild) - A Comprehensive and Hackable Build System for Multilingual Python Packages: Cython (including automatic conversion from Python to Cython), C/C++, Objective-C, Go, and Nim, with ongoing expansions to include additional languages. (Planned to be released soon) 
* [cengal_app_dir_path_finder](https://github.com/FI-Mihej/cengal_app_dir_path_finder) - A Python module offering a unified API for easy retrieval of OS-specific application directories, enhancing data management across Windows, Linux, and macOS 
* [cengal_cpu_info](https://github.com/FI-Mihej/cengal_cpu_info) - Extended, cached CPU info with consistent output format.
* [cengal_memory_barriers](https://github.com/FI-Mihej/cengal_memory_barriers) - Fast crossplatform memory barriers for Python.
* [flet_async](https://github.com/FI-Mihej/flet_async) - wrapper which makes [Flet](https://github.com/flet-dev/flet) async and brings booth Cengal.coroutines and asyncio to Flet (Flutter based UI)
* [justpy_containers](https://github.com/FI-Mihej/justpy_containers) - wrapper around [JustPy](https://github.com/justpy-org/justpy) in order to bring more security and more production-needed features to JustPy (VueJS based UI)
* [Bensbach](https://github.com/FI-Mihej/Bensbach) - decompiler from Unreal Engine 3 bytecode to a Lisp-like script and compiler back to Unreal Engine 3 bytecode. Made for a game modding purposes
* [Realistic-Damage-Model-mod-for-Long-War](https://github.com/FI-Mihej/Realistic-Damage-Model-mod-for-Long-War) - Mod for both the original XCOM:EW and the mod Long War. Was made with a Bensbach, which was made with Cengal
* [SmartCATaloguer.com](http://www.smartcataloguer.com/index.html) - TagDB based catalog of images (tags), music albums (genre tags) and apps (categories)

# License

Copyright © 2012-2024 ButenkoMS. All rights reserved.

Licensed under the Apache License, Version 2.0.
