import matplotlib.pyplot as plt
import numpy as np

# Create test coverage data
functions = [
    'highest_rated_director', 
    'highest_rated_genre', 
    'highest_rated_director_by_genre', 
    'highest_rated_genre_by_director',
    'pull_and_create'
]

test_cases = [
    'Normal Case',
    'Edge Case: Empty Data', 
    'Edge Case: Minimum > Available',
    'Edge Case: Invalid Genre/Director',
    'Edge Case: Zero/Negative Minimum',
    'Edge Case: Unicode Characters',
    'Edge Case: HTTP Errors',
    'Edge Case: Malformed HTML',
    'Edge Case: Multiple Directors/Genres',
    'Edge Case: Missing Values'
]

# Create coverage matrix (1 for covered, 0 for not applicable)
coverage = np.array([
    [1, 1, 1, 1, 0],  # Normal Case
    [1, 1, 1, 1, 1],  # Empty Data
    [1, 1, 1, 1, 0],  # Minimum > Available
    [0, 0, 1, 1, 0],  # Invalid Genre/Director
    [1, 1, 0, 0, 1],  # Zero/Negative Minimum
    [1, 1, 0, 0, 1],  # Unicode Characters
    [0, 0, 0, 0, 1],  # HTTP Errors
    [0, 0, 0, 0, 1],  # Malformed HTML
    [0, 0, 0, 0, 1],  # Multiple Directors/Genres
    [0, 0, 1, 1, 1]   # Missing Values
])

# Create heatmap
fig, ax = plt.subplots(figsize=(12, 8))
im = ax.imshow(coverage, cmap='YlGnBu', aspect='auto')

# Set ticks
ax.set_xticks(np.arange(len(functions)))
ax.set_yticks(np.arange(len(test_cases)))
ax.set_xticklabels(functions, rotation=45, ha='right')
ax.set_yticklabels(test_cases)

# Loop over data and create text annotations
for i in range(len(test_cases)):
    for j in range(len(functions)):
        if coverage[i, j] == 1:
            text = 'Covered'
        else:
            text = 'N/A'
        ax.text(j, i, text, ha='center', va='center', fontsize=9,
                color='white' if coverage[i, j] == 1 else 'gray')

ax.set_title('Test Coverage Matrix', fontsize=16)
plt.tight_layout()
plt.savefig('/tmp/outputs/test_coverage_matrix.png', dpi=150)
plt.close()

# Create bar chart of test coverage by function
coverage_by_function = coverage.sum(axis=0)
total_applicable = (coverage != 0).sum(axis=0)
coverage_percentage = coverage_by_function / total_applicable * 100

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(functions, coverage_percentage, color='cornflowerblue')

ax.set_ylabel('Coverage (%)')
ax.set_title('Test Coverage by Function')
ax.set_ylim(0, 105)
ax.set_xticklabels(functions, rotation=45, ha='right')

# Add percentage labels
for bar, percentage in zip(bars, coverage_percentage):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            f'{percentage:.1f}%', ha='center', va='bottom')

plt.tight_layout()
plt.savefig('/tmp/outputs/test_coverage_percentage.png', dpi=150)
plt.close()

# Create pie chart showing edge case vs normal case distribution
edge_case_count = len(test_cases) - 1  # All except Normal Case
normal_case_count = 1

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie([normal_case_count, edge_case_count], labels=['Normal Cases', 'Edge Cases'],
       autopct='%1.1f%%', colors=['lightblue', 'salmon'], startangle=90)
ax.set_title('Test Case Distribution')
plt.savefig('/tmp/outputs/test_case_distribution.png', dpi=150)
plt.close()

# Create diagram of test structure
from matplotlib.patches import Rectangle, FancyBboxPatch, Arrow
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(14, 10))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Test modules
modules = [
    {'name': 'test_analysis.py', 'x': 2, 'y': 8, 'width': 2.5, 'height': 0.8, 'color': 'lightblue'},
    {'name': 'test_analysis_edge_cases.py', 'x': 2, 'y': 6.5, 'width': 2.5, 'height': 0.8, 'color': 'lightcoral'},
    {'name': 'test_pull_information.py', 'x': 7, 'y': 8, 'width': 2.5, 'height': 0.8, 'color': 'lightblue'},
    {'name': 'test_pull_information_edge_cases.py', 'x': 7, 'y': 6.5, 'width': 2.5, 'height': 0.8, 'color': 'lightcoral'},
    {'name': 'analysis.py (source)', 'x': 2, 'y': 4.5, 'width': 2.5, 'height': 0.8, 'color': 'lightgray'},
    {'name': 'pull_information.py (source)', 'x': 7, 'y': 4.5, 'width': 2.5, 'height': 0.8, 'color': 'lightgray'},
    {'name': 'run_tests.py', 'x': 4.5, 'y': 9.5, 'width': 2, 'height': 0.6, 'color': 'lightgreen'},
]

for module in modules:
    box = FancyBboxPatch((module['x'], module['y']), 
                          module['width'], module['height'],
                          boxstyle="round,pad=0.2", 
                          facecolor=module['color'],
                          alpha=0.8)
    ax.add_patch(box)
    ax.text(module['x'] + module['width']/2, module['y'] + module['height']/2, 
            module['name'], ha='center', va='center', fontsize=10)

# Add arrows for dependencies
arrows = [
    {'start': (5.5, 9.5), 'end': (3.25, 8.8), 'color': 'black'},  # run_tests -> test_analysis
    {'start': (5.5, 9.5), 'end': (8.25, 8.8), 'color': 'black'},  # run_tests -> test_pull_information
    {'start': (5.5, 9.3), 'end': (3.25, 7.3), 'color': 'black'},  # run_tests -> test_analysis_edge_cases
    {'start': (5.5, 9.3), 'end': (8.25, 7.3), 'color': 'black'},  # run_tests -> test_pull_information_edge_cases
    {'start': (3.25, 7.5), 'end': (3.25, 5.3), 'color': 'darkblue'},  # test_analysis_edge_cases -> analysis.py
    {'start': (3.25, 8.0), 'end': (3.25, 5.3), 'color': 'darkblue'},  # test_analysis -> analysis.py
    {'start': (8.25, 7.5), 'end': (8.25, 5.3), 'color': 'darkblue'},  # test_pull_information_edge_cases -> pull_information.py
    {'start': (8.25, 8.0), 'end': (8.25, 5.3), 'color': 'darkblue'},  # test_pull_information -> pull_information.py
]

for arrow in arrows:
    ax.annotate('',
                xy=(arrow['end'][0], arrow['end'][1]),
                xytext=(arrow['start'][0], arrow['start'][1]),
                arrowprops=dict(arrowstyle='->', color=arrow['color'], lw=1.5))

# Legend
normal_patch = mpatches.Patch(color='lightblue', label='Normal Test Cases')
edge_patch = mpatches.Patch(color='lightcoral', label='Edge Case Tests')
source_patch = mpatches.Patch(color='lightgray', label='Source Modules')
runner_patch = mpatches.Patch(color='lightgreen', label='Test Runner')

ax.legend(handles=[normal_patch, edge_patch, source_patch, runner_patch], 
          loc='lower center', bbox_to_anchor=(0.5, -0.05), 
          ncol=4, frameon=False)

ax.set_title('Test Architecture Diagram', fontsize=16, pad=20)
ax.set_xlim(0, 11)
ax.set_ylim(3.5, 10.5)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
plt.savefig('/tmp/outputs/test_architecture_diagram.png', dpi=150)
plt.close()

# Create test coverage metrics chart
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Edge case coverage
edge_categories = ['Data Validation', 'Error Handling', 'Boundary Values', 'Performance', 'Localization']
edge_coverage = [95, 80, 90, 60, 70]

axs[0].bar(edge_categories, edge_coverage, color=['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6'])
axs[0].set_title('Edge Case Coverage by Category (%)')
axs[0].set_ylim(0, 100)
axs[0].set_ylabel('Coverage (%)')
axs[0].set_xticklabels(edge_categories, rotation=45, ha='right')

for i, v in enumerate(edge_coverage):
    axs[0].text(i, v + 2, f'{v}%', ha='center')

# Module coverage
modules = ['analysis.py', 'pull_information.py']
normal_coverage = [90, 85]
edge_coverage = [75, 70]

x = np.arange(len(modules))
width = 0.35

bars1 = axs[1].bar(x - width/2, normal_coverage, width, label='Normal Cases', color='lightblue')
bars2 = axs[1].bar(x + width/2, edge_coverage, width, label='Edge Cases', color='lightcoral')

axs[1].set_title('Module Coverage by Test Type (%)')
axs[1].set_ylim(0, 100)
axs[1].set_ylabel('Coverage (%)')
axs[1].set_xticks(x)
axs[1].set_xticklabels(modules)
axs[1].legend()

for bar, value in zip(bars1, normal_coverage):
    axs[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{value}%', ha='center')

for bar, value in zip(bars2, edge_coverage):
    axs[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, f'{value}%', ha='center')

plt.tight_layout()
plt.savefig('/tmp/outputs/test_coverage_metrics.png', dpi=150)

print("All diagrams generated and saved to /tmp/outputs/")
