from solver.solver import perform_solving
import matplotlib.pyplot as plt
import numpy as np

L_Blair, L_Bell, L_Evanschitzky, L_Evanschitzky_Temp = perform_solving()

plt.figure(figsize=(10, 6))  # Sets a nice, readable window size

plt.plot(L_Blair, label='Blair', linewidth=2)
plt.plot(L_Bell, label='Bell', linewidth=2)
plt.plot(L_Evanschitzky, label='Evanschitzky', linewidth=2)
plt.plot(L_Evanschitzky_Temp, label = "Evanschitzky accounted for temp change", linewidth=2)

plt.title('Comparison of Solver Results', fontsize=14, fontweight='bold')
plt.xlabel('RPM', fontsize=12)
plt.ylabel('Length', fontsize=12)

plt.legend(loc='best')
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()