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

import:
```py
from folder_dict import FolderDict
```

# Usage
- import and construct  
    ```py
    # Empty Folder Dict
    fd = FolderDict(sep="/")
    > fd
    --> FolderDict({})
    ```

- reference  
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

    > fd["friend/Ben"]
    --> FolderDict({
        "age": 30,
    })
    ```

    - multiple input  
        ```py
        > fd["name", "age","friends/Ben/age"]
        --> ("Joe", 22, 35)
        ```


- subcribe  
    ```py
    fd = FolderDict(sep="/")
    fd["path/to/obj_name"] = 10
    
    > fd["path/to/obj_name"]
    10
    ```
    - multiple  
    ```py
    fd["a/b", "c/d"] = (0,1)
    > fd
    --> FolderDict({
        "a/b": 0,
        "c/d": 1
    })
    ```

- listup  
    ```py
    fd["a/b", "c/d"] = (0,1)
    > fd.listup()
    --> ["a/b", "c/d"]
    ```

- wild card of listup()   
    ```py
    fd["a/b/c.d", "a/b/e.d"] = (10,20)
    > fd.listup("a/**/*.d")
    --> ["a/b/c.d", "a/b/e.d"] 
    ```

- "~" path  
    Get paths ending with "c".
    ```py
    fd["a/b/c", "d/e/f/abc", "g/h/c", "i/j"] = (1,2,3,4)
    > fd.listup("~c")
    --> ["a/b/c", "d/e/f/abc", "g/h/c"]
    ```
    *cf.*
    ```py
    > fd.listup("~/c")
    --> ["a/b/c", "g/h/c"]
    ```

- All combinations  
    ```py
    fd["a/b/c.md","x/y/z", "a/d/e/f.md"] = (0,1,2)
    > fd.listup("a/~/*.md")
    ["a/b/c.md", "a/d/e/f.md"]
    ```

- dict and path_dict
    ```py
    fd["a/b","a/c"] = (1,2)
    > fd.dict
    --> {'a': {'b': 1, 'c': 2}}

    > fd.PathDict
    -->PathDict({
      "a": {
        "b": 1,
        "c": 2  
      }
    })
    ```

