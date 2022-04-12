# Folder Dict
The versatile dict for Python!

# Installation
```
pip install folder-dict
```
or clone this repository and run the following command.
```
pip install -e ./
```

Import
```py
from folder_dict import FolderDict
```

# Usage
- Import and Construct  
    ```py
    # Empty Folder Dict
    fd = FolderDict(sep="/")
    > fd
    --> FolderDict({})
    ```

- Subscription  
    ```py 
    user =  {
	    "name": "Joe",
    	"age": 22,
    	"hobbies": ["Playing football", "Podcasts"],
	    "friends": {
    		"Sue": {"age": 30},
	    	"Ben": {"age": 35},
    	    }
    }

    fd = FolderDict(user, sep="/")
    > fd["name"]
    --> Joe
    
    > fd["friend/Sue/age"]
    --> 30

    > fd["/friend/Ben"]
    --> FolderDict({
        "age": 30,
    })
    ```

    - Multiple inputs 
        ```py
        > fd["name", "age","friends/Ben/age"]
        --> ("Joe", 22, 35)
        ```


- Assignment  
    Assigns the object at the given path into the FolderDict.
    ```py
    fd = FolderDict(sep="/")
    fd["path/to/obj_name"] = 10
    
    > fd["path/to/obj_name"]
    10
    ```
    - Multiple inputs  
    ```py
    fd["a/b", "c/d"] = (0,1)
    > fd
    --> FolderDict({
        "a/b": 0,
        "c/d": 1
    })
    ```

- list
    Lists all paths contained in the FolderDict.
    ```py
    fd["a/b", "c/d"] = (0,1)
    > fd.list()
    --> ["/a/b", "/c/d"]
    ```

- Direct card `~`  
    Get paths ending with "c".
    ```py
    fd["a/b/c", "d/e/f/abc", "g/h/c", "i/j"] = (1,2,3,4)
    > fd.list("~c")
    --> ["/a/b/c", "/d/e/f/abc", "/g/h/c"]
    ```
    *cf.*
    ```py
    > fd.list("~/c")
    --> ["a/b/c", "g/h/c"]
    ```

- Properties
    ```py
    fd["a/b","a/c"] = (1,2)

    # dict
    > fd.dict
    --> {'a': {'b': 1, 'c': 2}}
    
    # PathDict
    > fd.PathDict
    -->PathDict({
      "a": {
        "b": 1,
        "c": 2  
      }
    })

    # sep
    > fd.sep
    --> '/'
    ```

