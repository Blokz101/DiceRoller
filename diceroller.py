from functools import lru_cache
import math
import re
import random
import readline
import os

class DiceRoller:
    
    inputPatternRegEx: str = "\d+d\d+((\+|\-)\d+)?"
    
    
    
    def main():
        
        while True:
            
            # Get the next input from the user
            line: str = input("\n>>> ")
            os.system("clear")
            
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
            addedModifier: bool = ( len(inputs) == 3 )
            
            #Set the modifier to 0 if there is none given
            if not addedModifier:
                inputs.append(0)
            
            # Negate the modifier if it should be negative
            if addedModifier and "-" in line:
                inputs[2] *= -1
            
            #Set dice values based on inputs
            numDice: int = inputs[0]
            diceMax: int = inputs[1]
            modifier: int = inputs[2]
            
            
            
            # Print the roll status
            print("\nRolling {0} d{1} with {2:+} modifier".format(
                numDice,
                diceMax,
                modifier
            ))  
            
            # Print roll table headers
            print("\n{0:<10}{1}".format("Roll #", "Value"))
            print("------------------")
            
            # Roll and sum the dice
            diceSum: int = 0
            for index in range(numDice):
                
                diceRoll: int = random.randint(1, diceMax)
                diceSum += diceRoll
                
                print("{0:<10}{1}".format("Roll " + str(index + 1), diceRoll))



            print("\n{0:<12}{1}".format("Dice Sum", diceSum))
            print("{0:<12}{1:+}".format("Modifier", modifier))
            print("{0:<12}{1}".format("Total", diceSum + modifier))
            
            
            print("\nRoll Stastics")
            print("--------------------------------")
            print("{0:<25}{1}".format("Roll Max", round(
                numDice * diceMax
            )))
            print("{0:<25}{1}".format("Roll Average", round(
                ((diceMax + 1) / 2) * numDice, 4
            )))
            print("{0:<25}{1}".format("Roll Min", round(
                numDice
            )))
            print("{0:<25}{1}".format("Standard Deviation", round(
                DiceRoller.standardDeviation(numDice, diceMax), 4
            )))
            print("{0:<25}{1}".format("Probability = X", round(
                DiceRoller.sumProbability(diceSum, numDice, diceMax) * 100, 4
            )))
            print("{0:<25}{1}".format("Probability ≤ X", round(
                DiceRoller.sumAndBelowProbability(diceSum, numDice, diceMax) * 100, 4
            )))
            print("{0:<25}{1}".format("Probability ≥ X", round(
                DiceRoller.sumAndAboveProbability(diceSum, numDice, diceMax) * 100, 4
            )))
                    
                    
                
                
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
    DiceRoller.main()