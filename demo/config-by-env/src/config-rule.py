class ConfigurationRule:

    def ___init___(
            self, 
            name: str, 
            vtype: str = "str", 
            vregex = None, 
            required: bool = False, 
            min = None, 
            max = None
        ):
        self.name = name
        self.vtype = vtype
        self.vregex = vregex
        self.required = required
        self.min = min
        self.max = max

