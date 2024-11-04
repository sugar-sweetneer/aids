!pip install scikit-fuzzy
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
# Define universe of discourse
x = np.arange(0, 11, 1)
# Define fuzzy sets A and B
A = fuzz.trimf(x, [0, 5, 10])
B = fuzz.trimf(x, [5, 10, 10])
# Calculate Union
A_union_B = np.maximum(A, B)
# Calculate Intersection
A_intersection_B = np.minimum(A, B)
# Calculate Complement of A
A_complement = 1 - A
# Calculate Complement of B
B_complement = 1 - B
# Calculate Difference (A - B)
A_difference_B = np.maximum(A - B, 0)
# Calculate Algebraic Sum
A_algebraic_sum = np.minimum(A + B, 1)
# Calculate Algebraic Difference
A_algebraic_difference = np.maximum(A + B - 1, 0)
# Calculate Bounded Sum
A_bounded_sum = np.minimum(A + B, 1)
# Calculate Bounded Difference
A_bounded_difference = np.maximum(A - B, 0)
# Fuzzy Cartesian Product
cartesian_product = np.array([[min(a, b) for b in B] for a in A])
# Fuzzy Aggregation (Weighted Average)
weights = [0.6, 0.4]  # Weights for A and B
weighted_aggregation = weights[0] * A + weights[1] * B
# Plotting the results
plt.figure(figsize=(12, 8))
# Plot A and B
plt.subplot(4, 3, 1)
plt.title('Fuzzy Set A and B')
plt.plot(x, A, 'r', label='A')
plt.plot(x, B, 'b', label='B')
plt.legend()
plt.subplot(3, 3, 2)
plt.title('Union A ∪ B')
plt.plot(x, A_union_B, 'g', label='A ∪ B')
plt.legend()
plt.subplot(3, 3, 3)
plt.title('Intersection A ∩ B')
plt.plot(x, A_intersection_B, 'c', label='A ∩ B')
plt.legend()
plt.subplot(3, 3, 4)
plt.title('Complement of A')
plt.plot(x, A_complement, 'm', label='¬A')
plt.legend()
plt.subplot(4, 3, 5)
plt.title('Complement of B')
plt.plot(x, B_complement, 'orange', label='¬B')
plt.legend()
plt.subplot(3, 3, 5)
plt.title('Difference A - B')
plt.plot(x, A_difference_B, 'y', label='A - B')
plt.legend()
plt.subplot(3, 3, 6)
plt.title('Algebraic Sum A ⊕ B')
plt.plot(x, A_algebraic_sum, 'k', label='A ⊕ B')
plt.legend()
plt.subplot(3, 3, 7)
plt.title('Algebraic Difference A ⊖ B')
plt.plot(x, A_algebraic_difference, 'orange', label='A ⊖ B')
plt.legend()
plt.subplot(3, 3, 8)
plt.title('Bounded Sum A ⊕ B (bounded)')
plt.plot(x, A_bounded_sum, 'purple', label='Bounded A ⊕ B')
plt.legend()
plt.subplot(3, 3, 9)
plt.title('Bounded Difference A ⊖ B (bounded)')
plt.plot(x, A_bounded_difference, 'brown', label='Bounded A ⊖ B')
plt.legend()
# Plot Weighted Aggregation
plt.subplot(3, 3, 4)
plt.title('Weighted Aggregation')
plt.plot(x, weighted_aggregation, 'm', label='Weighted A + B')
plt.legend()
# Show the cartesian product in a heatmap
plt.subplot(3, 3, 5)
plt.title('Fuzzy Cartesian Product')
plt.imshow(cartesian_product, extent=[0, 10, 0, 10], origin='lower', aspect='auto')
plt.colorbar(label='Membership Degree')
plt.xlabel('A')
plt.ylabel('B')
plt.tight_layout()
plt.show()
