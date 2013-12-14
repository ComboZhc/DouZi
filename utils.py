from web.utils import safeunicode

class Storage(dict):
    def __getattr__(self, key): 
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __setattr__(self, key, value): 
        self[key] = value
    
    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k
    
    def __repr__(self):     
        return '<Storage ' + dict.__repr__(self) + '>'

def _storify(mapping):
    stor = Storage()
    for key in mapping.keys():
        value = mapping[key]
        if isinstance(value, list):
            value = [_storify(x) for x in value]
        setattr(stor, key, value)    
    return stor

def storify(mapping):
    if isinstance(mapping, dict):
        return _storify(mapping)
    if isinstance(mapping, list):
        return [_storify(x) for x in mapping]