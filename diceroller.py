from functools import lru_cache
import math
import re
import random
from rich.console import Console
from rich.table import Table
from rich import box
import os

if os.name == "posix":
    import readline
elif os.name == "nt":
    import pyreadline3
else:
    raise OSError("Operating System is not compatable")



class DiceRoller:
    
    inputPatternRegEx: str = "\d+d\d+((\+|\-)\d+)?"
    
    
    def __init__(self) -> None:
        
        self.console = Console()
        
    
    
    def main(self):
        
        while True:
            
            # Get the next input from the user
            line: str = input("\n>>> ")
            
            if os.name == "posix":
                os.system("clear")
            if os.name == "nt":
                os.system("cls")
            
            # Quit if the input is q
            if re.fullmatch("exit|q|stop", line):
                break
        
            # Check if the input is valid
            if not re.fullmatch(DiceRoller.inputPatternRegEx, line):
                print("Input not valid")
                continue
            
            
            
            # Split input into numbers
            inputs: list[int] = [int(num) for num in re.findall("\d+", line)]
            
            # Set the added modifier boolean
            addedModifier: bool = (len(inputs) == 3)
            
            #Set the modifier to 0 if there is none given
            if not addedModifier:
                inputs.append(0)
            
            # Negate the modifier if it should be negative
            if addedModifier and "-" in line:
                inputs[2] *= -1
            
            self.rollDice(inputs[0], inputs[1], inputs[2])
            
            
            
    def rollDice(self, numDice: int, diceMax: int, modifier: int) -> None:
        
            # Print the roll status
            print("\nRolling {0} d{1} with {2:+} modifier".format(
                numDice,
                diceMax,
                modifier
            ))  
            
            # Define the roll table
            rollTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)
            rollTable.add_column("Roll #", no_wrap = True, width = 10, footer = "Raw Total")
            rollTable.add_column("Value", no_wrap = True, width = 10)
            rollTable.add_column("Sum", no_wrap = True, width = 10)
            
            # Roll and sum the dice
            diceSum: int = 0
            for index in range(numDice):
                
                diceRoll: int = random.randint(1, diceMax)
                diceSum += diceRoll
                
                rollTable.add_row("Roll {0}".format(index), str(diceRoll), str(diceSum))
                
            # Print the table
            rollTable.columns[2].footer = str(diceSum)
            self.console.print(rollTable)
            
            # Define the statsitcs table
            stasticsTable: Table = Table(box = box.SIMPLE_HEAD)
            stasticsTable.add_column("Roll Stastics", no_wrap = True, width = 20)
            stasticsTable.add_column("", no_wrap = True, width = 10)
            
            # Calculate the statsitcs for the roll
            stasticsTable.add_row("Roll Max", str(round( numDice * diceMax, 4 )) )
            stasticsTable.add_row("Roll Mean", str(round( ((diceMax + 1) / 2) * numDice, 4 )) )
            stasticsTable.add_row("Roll Min", str(round( numDice, 4 )) )
            stasticsTable.add_row("Standard Deviation",  str(round( DiceRoller.standardDeviation(numDice, diceMax), 4 )) )
            stasticsTable.add_row("Probability = X",  str(round( DiceRoller.sumProbability(diceSum, numDice, diceMax) * 100, 4 )) )
            stasticsTable.add_row("Probability ≤ X",  str(round( DiceRoller.sumAndBelowProbability(diceSum, numDice, diceMax) * 100, 4 )) )
            stasticsTable.add_row("Probability ≥ X",  str(round( DiceRoller.sumAndAboveProbability(diceSum, numDice, diceMax) * 100, 4 )) )
            
            # Print the table
            self.console.print(stasticsTable)   
            
            # Define the final numbers table
            finalTable: Table = Table(box = box.SIMPLE_HEAD, show_footer = True)  
            finalTable.add_column("Final Numbers", no_wrap = True, width = 20, footer = "Final Total")
            finalTable.add_column("", no_wrap = True, width = 10)
                
            # Add values
            finalTable.add_row("Dice Sum", str( diceSum ))
            finalTable.add_row("Modifier", "{:+}".format(modifier))
            
            # Print table
            finalTable.columns[1].footer = str(diceSum + modifier)
            self.console.print(finalTable)
                
                
                
    @classmethod
    def standardDeviation(cls, numDice: int, diceMax: int) -> float:
        
        variance: float = numDice * (diceMax**2 - 1) / 12
        
        return math.sqrt(variance)
    
    
    
    @classmethod
    def sumProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        return DiceRoller.__sumsForTotal(total, numDice, diceMax) / diceMax**numDice
    
    
    
    @classmethod
    def sumAndAboveProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        if total == numDice * diceMax:
            return DiceRoller.sumProbability(numDice, numDice, diceMax)
        
        return DiceRoller.sumProbability(total, numDice, diceMax) + DiceRoller.sumAndAboveProbability(total + 1, numDice, diceMax)
    
    
    
    @classmethod
    def sumAndBelowProbability(cls, total: int, numDice: int, diceMax: int) -> float:
        
        if total == numDice:
            return DiceRoller.sumProbability(numDice, numDice, diceMax)
        
        return DiceRoller.sumProbability(total, numDice, diceMax) + DiceRoller.sumAndBelowProbability(total - 1, numDice, diceMax)
    
    
    
    @classmethod
    @lru_cache(None)
    def __sumsForTotal(cls, total: int, numDice: int, diceMax: int) -> int:
        
        if not numDice:
            return not total
        
        return sum( DiceRoller.__sumsForTotal( total - die, numDice - 1, diceMax) for die in range(1, diceMax + 1) )
        
        
        
    
    

if __name__ == "__main__":
    DiceRoller().main()