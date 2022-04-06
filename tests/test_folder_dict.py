from folder_dict import __version__, FolderDict
from path_dict import PathDict

user =  {
    "name": "Joe",
	"age": 22,
	"hobbies": ["Playing football", "Podcasts"],
    "friends": {
		"Sue": {"age": 30},
    	"Ben": {"age": 35},
	    }
}


def test_version():
    assert __version__ == '0.1.0'

def test_constructor():
    """testing constructor"""
    fd = FolderDict()
    # data is path_dict
    assert isinstance(fd.data, PathDict)
    fd_2 = FolderDict(fd)
    assert isinstance(fd_2.data, PathDict)
    fd = FolderDict(user)
    assert isinstance(fd.data, PathDict)

    # deep copy
    fd_same = FolderDict(fd, deep_copy=False)
    assert (fd.data is fd_same.data)
    fd_copy = FolderDict(fd, deep_copy=True)
    assert not (fd.data is fd_copy.data)
    


def test_property():
    """tests properties of FolderDict."""
    # sep
    fd = FolderDict(user, sep="/")
    assert fd.sep == "/"
    assert fd.sep != "."
    fd = FolderDict(user, sep=".")
    assert fd.sep == "."
    assert fd.sep != "a"
    fd = FolderDict(user, sep="!")
    assert fd.sep == "!"

    # dict
    fd = FolderDict(user, deep_copy=False)
    assert fd.dict is user
    assert fd.dict == user

    # path_dict
    fd = FolderDict(user)
    path_dict_user = PathDict(user)
    assert fd.path_dict == path_dict_user
    assert isinstance(fd.path_dict, PathDict)

