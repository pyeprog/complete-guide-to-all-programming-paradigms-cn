def sqrt(x):
    def improve(guess: float) -> float:
        return (guess + x / guess) / 2.0
    
    def good_enough(guess: float) -> bool:
        return abs(guess * guess - x) / x < 0.00001
    
    def sqrt_iter(guess):
        return guess if good_enough(guess) else sqrt_iter(improve(guess))
    
    return sqrt_iter(1.0)