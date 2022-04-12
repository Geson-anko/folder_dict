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

def test_parse_path():
    fd = FolderDict(user, sep="/")
    assert fd.parse_path("name") == ["name"]
    assert fd.parse_path("a/b") == ["a","b"]
    assert fd.parse_path("a/b/c") == ["a","b","c"]
    assert fd.parse_path("/a/b") == ["a","b"]
    assert fd.parse_path("/a/b/c/") == ["a","b","c"]


def test_get_path():
    fd = FolderDict(user,sep="/")
    assert fd.get_path("name") == "Joe"
    assert fd.get_path("friends/Sue/age") == 30
    assert fd.get_path("friends/Sue/age/") == 30
    assert fd.get_path("friends/Ben/age") == 35
    assert fd.get_path("/friends/Ben/age") == 35

    fd = FolderDict(user,sep=".")
    assert fd.get_path("friends.Sue.age")
    assert fd.get_path("friends.Ben.age")
    assert fd.get_path(".friends.Ben.age")
    assert fd.get_path(".friends.Ben.age.")
    assert fd.get_path("friends.Ben.age.")

def test_set_path():
    fd = FolderDict(sep="/")
    fd.set_path("a",10)
    fd.set_path("b/c",20)
    fd.set_path("b/d",30)
    fd.set_path("/e/f/g/h", 40)
    
    assert fd.get_path("a") == 10
    assert fd.get_path("b/c") == 20
    assert fd.get_path("b").get_path("d") == 30
    assert fd.get_path("e/f/g/h/") == 40

def test___getitem__():
    fd = FolderDict(user, sep="/")
    
    assert fd["name"] == "Joe"
    assert fd["friends/Sue/age"] == 30
    assert fd["hobbies", "age"] == [["Playing football", "Podcasts"], 22]
    assert fd["age", "/name"] == [22, "Joe"]
    assert fd[("age", "name")] == [22, "Joe"]


def test__setitem__():
    fd = FolderDict(sep="/")
    fd["a"] = 10
    fd["b/c"] = 20
    fd["d","e/f"] = 30,40
    fd[["b/g", "h/i/j"]] = 50,60
    
    assert fd["b/c"] == 20
    assert fd["a"] == 10
    assert fd["d"] == 30
    assert fd["e/f"] == 40
    assert fd["b/g"] == 50
    assert fd["h/i/j"] == 60

def test_list_all():
    fd = FolderDict(user, sep="/")
    paths = fd.list_all()
    assert not "name" in paths
    assert "/name" in paths
    assert "/age" in paths
    assert "/hobbies" in paths
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not "friends/Ben/age" in paths
    assert not '/friends/Sue' in paths
    assert not '/friends/Ben' in paths
    assert not "/friends" in paths
    assert not "/" in paths

    fd = FolderDict(user, sep=".")
    paths = fd.list_all()
    assert ".friends.Sue.age" in paths
    assert not "/friends/Ben/age" in paths
    assert not 'friends.Sue' in paths
    assert not 'friends.Ben' in paths

def test_clean_path():
    fd = FolderDict(sep="/")

    assert fd.clean_path("/a/b") == "/a/b"
    assert fd.clean_path("/a/") == "/a"
    assert fd.clean_path("a/b/c/") == "/a/b/c"

    fd = FolderDict(sep=".")
    assert fd.clean_path("a.b.") == ".a.b"
    assert fd.clean_path(".s") == ".s"
    assert fd.clean_path("s.v.f.") == ".s.v.f"

def test_paths():
    fd = FolderDict(user,sep="/")
    fd["sex/real"] = "male"
    fd["/sex/virtual"] = "female"
    
    paths = fd.paths
    assert "/name" in paths
    assert "/age" in paths
    assert "/hobbies" in paths
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not '/friends/Sue' in paths
    assert not '/friends/Ben' in paths
    assert not "/friends" in paths
    assert not "/" in paths
    assert "/sex/real" in paths
    assert not "/sex" in paths
    assert not "sex/virtual/" in paths
    assert not "/sex/virtual/" in paths
    assert "/sex/virtual" in paths

def test_join():
    fd = FolderDict(sep="/")
    assert fd.join("a","b") == "/a/b"
    assert fd.join("a") == "/a"
    assert fd.join("a","b","c/d/") == "/a/b/c/d"
    
    fd = FolderDict(sep=".")
    assert fd.join("a","b") == ".a.b"
    assert fd.join("a.b.","c.d") == ".a.b.c.d"


def test_direct_card():
    fd = FolderDict(user, sep="/")
    
    paths = fd.direct_card("~/age")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths
    
    paths = fd.direct_card("frie~")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths

    paths = fd.direct_card("friends/~/age")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths

    paths = fd.direct_card("name")
    assert "/name" in paths
    assert not "/friends/Sue/age" in paths

def test_list():

    # pathname is None
    fd = FolderDict(user,sep="/")

    # None
    paths = fd.list()
    assert paths == fd.paths

    # normal 
    paths = fd.list("friends")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths

    # direct card
    paths = fd.list("frie~")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert not "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths

    paths = fd.list("~/age")
    assert "/friends/Sue/age" in paths
    assert "/friends/Ben/age" in paths
    assert "/age" in paths
    assert not "/name" in paths
    assert not "/hobbies" in paths
