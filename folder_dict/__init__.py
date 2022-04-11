from __future__ import annotations

__version__ = '0.1.0'

from path_dict import PathDict
from typing import *
from copy import deepcopy
class FolderDict:
    """
    Folder Dict is a wrapper for PathDict that allows 
    you to register objects in a file path-like format string.
    """
    def __init__(
        self, data:Union[dict, PathDict, FolderDict]= {}, deep_copy:bool=False,*,sep:str="/"
        ) -> None:
        """
        Initialize with a dict, PathDict or another FolderDict.
		This will reference the original it,
		so changes will also happen to them.
		If you do not want this set deep_copy to True.
        """
        if isinstance(data, FolderDict):
            self.data = data.path_dict
        elif isinstance(data, PathDict):
            self.data = data
        elif isinstance(data, dict):
            self.data = PathDict(data)
        else:
            raise TypeError("FolderDict init: data argument must be dict, PathDict or FolderDict.")

        if deep_copy:
            self.data = deepcopy(self.data)

        self.__sep = sep

        self.paths:List[str] = self.list_all()
    
    @property
    def sep(self) -> str:
        """returns the separator of path."""
        return self.__sep
    
    @property
    def dict(self) -> dict:
        """returns python dict."""
        return self.data.dict

    @property
    def path_dict(self) -> PathDict:
        """returns PathDict."""
        return self.data

    def parse_path(self, path:str) -> List[str]:
        """parsing path string and convert to list of str."""
        path_list = path.split(self.sep)
        
        if path_list[0] == "":
            path_list = path_list[1:]
        if path_list[-1] == "":
            path_list = path_list[:-1]
        
        return path_list

    def get_path(self, path:str) -> Any:
        """get subscribed object from path"""
        data = self.data[self.parse_path(path)]
        if isinstance(data, PathDict):
            return FolderDict(data)
        else:
            return data

    def set_path(self, path:str, value:Any) -> None:
        """set the value at the given path and append to `self.paths`"""
        path = self.clean_path(path)
        self.paths.append(path)
        self.data[self.parse_path(path)] = value

    def __getitem__(self, path:Union[str, Iterable[str]]) -> Union[Any, List[str]]:
        """
            Get the value at the given path.
            multiple subscriptions are supported, at which time
            the object of list is returned.
            <FolderDict>[path1, path2] -> [value1, value2]
        """
        
        if isinstance(path, str):
            return self.get_path(path)
        else:
            return [self.get_path(p) for p in path]

    def __setitem__(self, path:Union[str, Iterable[str]], value: Union[Any, Iterable[Any]]) -> None:
        """
            set the value at given paths.
            multiple reigistrations are supported.
            <FolderDict>[path1, path2] = value1, value2
        """
        if isinstance(path, str):
            return self.set_path(path, value)
        else:
            for (k,v) in zip(path, value):
                self.set_path(k,v)

    def list_all(self) -> List[str]:
        """
            This method returns all paths to objects 
            contained in the FolderDict.
        """
        return self._list_all(self.dict)
        
    def _list_all(self, d:dict) -> List[str]:
        """
            Runs internal processing of `self.list_all()`.
            This method recursivery lists all paths.
        """
        keys = d.keys()
        out = []
        for k in keys:
            value = d[k]
            if not isinstance(value, dict):
                out.append(k)
            else:
                v_keys = self._list_all(value)
                out += [f"{k}{self.sep}{i}" for i in v_keys]
        return out

    def clean_path(self, path:str) -> str:
        """
            This method cleans the path.
            "/a/b" -> "a/b"
            "b.c." -> "b.c"
        """
        if path[0] == self.sep:
            start = 1
        else:
            start = 0
        
        if path[-1] == self.sep:
            end = -1
        else:
            end = len(path)
        
        return path[start:end]