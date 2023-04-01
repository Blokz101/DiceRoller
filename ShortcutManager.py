import re



class ShortcutManager:
    
    def __init__(self, filename: str):

        self.shortcutDict: dict = {}
       
        with open(filename) as shortcutsFile:
            
            # Loop though all the lines in the csv file
            for line in shortcutsFile.readlines():
                
                tokens = re.split("\n|,", line)
                
                # Remove all empty strings from the tokens
                while "" in tokens:
                    tokens.remove("")
                
                # Make sure that there are the right number of tokens
                assert tokens and len(tokens) == 2, "Invalid syntax: {0}".format(line)
                
                self.shortcutDict[tokens[0]] = tokens[1]
                
                
                
    def match(self, line: str) -> str:
        
        return line in self.shortcutDict.keys()
    
    
    
    def getShortcut(self, key: str) -> str:
        
        return self.shortcutDict[key]
        
        
                  