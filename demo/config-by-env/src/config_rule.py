class ConfigurationRule:
    def __new__(cls,
            name: str, 
            vtype: str = "str", 
            vregex = None, 
            required: bool = False, 
            min = None, 
            max = None,
            vdefault = None
        ):
            instance = super().__new__(cls)
            instance.name = name
            instance.vtype = vtype
            instance.vregex = vregex
            instance.required = required
            instance.min = min
            instance.max = max
            instance.vdefault = vdefault
            return instance

    def ___init___(
            self, 
            name: str, 
            vtype: str = "str", 
            vregex = None, 
            required: bool = False, 
            min = None, 
            max = None,
            vdefault = None
        ):
        self.name = name
        self.vtype = vtype
        self.vregex = vregex
        self.required = required
        self.min = min
        self.max = max
        self.vdefault  = vdefault

    @classmethod
    def from_Args (
            cls,
            name: str, 
            vtype: str = "str", 
            vregex = None, 
            required: bool = False, 
            min = None, 
            max = None,
            vdefault = None
        ) :
        cr = ConfigurationRule(name)
        cr.vtype = vtype
        cr.vregex = vregex
        cr.required = required
        cr.min = min
        cr.max = max
        cr.vdefault = vdefault
        return cr