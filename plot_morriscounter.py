# DRIVER CODE
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axis import Axis

from morriscounter import MorrisCounter


def test(counter: MorrisCounter, n: int, axis: Axis) -> None:
  uppers, lowers, estimates, actuals = [], [], [], []
  for N in range(1, n+1):
    # incrementing counter function 
    counter.increment()
    # assert (1-counter.epsilon)*N <= counter.count <= (1+counter.epsilon)*N

    # Actual value of N
    actual = N
    # estimate of the counter
    estimate = counter.count
    # upper bound
    lower = (1-counter.epsilon)*N
    # lower bound
    upper = (1+counter.epsilon)*N

    # appending values in respective arrays.
    actuals.append(actual)
    estimates.append(estimate)
    lowers.append(lower)
    uppers.append(upper)

    # print(f"{actual=}, {estimate=:.8f} in [{lower:.8f}, {upper:.8f}]")
  # Ploting parameters
  MARKER_SIZE=.01
  LINE_WIDTH=.5
  axis.plot(actuals, estimates, label="estimate", marker="o", color="green", markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
  axis.plot(actuals, lowers, label="lower bound", color="red", linestyle="dashed", markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
  axis.plot(actuals, uppers, label="upper bound", color="red", linestyle="dashed", markersize=MARKER_SIZE, linewidth=LINE_WIDTH)
  axis.plot(actuals, actuals, label="actual", linestyle="dashed", color="grey", markersize=MARKER_SIZE, linewidth=LINE_WIDTH, alpha=0.3)
  axis.set_title(rf"$\varepsilon={counter.epsilon:.3g}$, $\delta={counter.delta:.3g}$", fontsize=6, y=-0.2)
  axis.axis('off')


# Driver Code - ploting data gathered above
if __name__ == '__main__':
  n = 10000
  bins = 5
  # This utility wrapper makes it convenient to create common layouts of subplots, including the enclosing figure object, in a single call.
  fig, axes = plt.subplots(bins, bins)
  # enumearate funciton creates objects with the list provided as argument
  # linspace returns evenly spaced numbers over the limits passed as argument
  for r, accuracy in enumerate(np.linspace(.5, .95, bins)):
    for c, max_failure_rate in enumerate(np.linspace(0.05, .45, bins)):
      print(f"{accuracy=}, {max_failure_rate=}")
      counter = MorrisCounter(accuracy=accuracy, max_failure_rate=max_failure_rate)
      test(counter, n=n, axis=axes[r][c])

  fig.suptitle(f"Morris(a) Counter, {n=}")
  handles, labels = axes[-1][-1].get_legend_handles_labels()
  fig.legend(handles, labels, loc='upper left', prop={'size': 6})
  fig.savefig("plots/morris-a.png", dpi=500)



