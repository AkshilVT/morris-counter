# import random module
from random import Random
# import typing from Optional module
from typing import Optional

# Defining class Morris Counter
class MorrisCounter:
  """An approximate counter.

  This is the Morris(a) counter.

  Let:
    * e = accuracy
    * d = max_failure_rate
    * a = 2*e^2*d

  After N increments:
    * the amount of space used is O(lglgN+lg(1/e)+lg(1/d)) with prob <= N*(1+a)^(-Z), where Z = (lgN/a)^C
    * the counter estimate N' satisfies Pr[|N-N'| > e*N] < d

  """
  # defining Counter
  X: float
  # defining Epsilon
  epsilon: float
  # defining Delta
  delta: float
  # defining a
  a: float
  # defining Random instance
  rng: Random
  #initation of the class Morris Counter
  def __init__(self, *, accuracy: float, max_failure_rate: float, rng: Optional[Random] = None) -> None:
    # asserting accuracy to be greater than 0.5 and less than 1
    assert 1/2 <= accuracy < 1, accuracy
    # asserting maximum failure rate to be greater than 0 and less than 0.5
    assert 0 < max_failure_rate < 1/2, max_failure_rate
    
    # INITALIZING epsilon
    self.epsilon = 1 - accuracy
    # INITALIZING delta
    self.delta = max_failure_rate
    # INITALIZING a
    self.a = 2 * self.epsilon ** 2 * self.delta
    #  returns a floating-point, pseudo-random number in the range 0 to less than 1 (inclusive of 0, but not 1) with approximately uniform distribution over that range
    self.rng = rng or Random()
    # INITALIZING counter
    self.X = 0
  
  # Increment function
  def increment(self) -> None:
    # Caliing increment function 
    if self._should_increment:
      self.X += 1


  # @property is a builtin function that creates and returns a property obect, has functions like fget(), fset(), fdel(), etc.
  
  @property
  def count(self) -> float:
    return self.a ** (-1) * ((1 + self.a) ** self.X - 1)

  @property
  def _increment_probability(self) -> float:
    return (1 + self.a) ** (-self.X)

  @property
  def _should_increment(self) -> bool:
    # Samples are uniformly distributed over the half-open interval [low, high) (includes low, but excludes high).
    return self.rng.uniform(0, 1) <= self._increment_probability
