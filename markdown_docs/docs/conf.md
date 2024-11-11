## FunctionDef get_version
**get_version**: The function of `get_version` is to retrieve the current version of the Discopy library.
**parameters**: This function does not take any parameters.
**Code Description**: 
The `get_version` function is defined without taking any arguments, making it a simple utility function. Inside the function, it imports the `__version__` attribute from the `discopy` module and returns this value directly. The `__version__` attribute is typically used in Python packages to store the version number of the package.

The use of `__version__` suggests that the Discopy library follows common practices for versioning, which often involves storing the version information as a string within the package's metadata. This allows developers and users to easily retrieve the current version without having to hard-code it in their scripts or applications.
**Note**: Ensure that the `discopy` module is properly installed and imported before calling this function. The returned value will be a string representing the library's version number, which can be useful for logging, debugging, or displaying information about the software being used.

**Output Example**: If the current version of Discopy is "0.9.5", then `get_version()` would return `"0.9.5"`.
