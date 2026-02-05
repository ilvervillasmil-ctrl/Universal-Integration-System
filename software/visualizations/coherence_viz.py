import matplotlib.pyplot as plt

# Constants
ALPHA = 26 / 27
BETA = 1 / 27

# Visualization of ALPHA and BETA
def plot_alpha_beta():
    """
    Visualizes the proportions of ALPHA (visible) and BETA (invisible) as a pie chart.
    """
    labels = ['ALPHA (Visible)', 'BETA (Invisible)']
    values = [ALPHA, BETA]
    colors = ['#4CAF50', '#FFC107']
    
    # Plot the pie chart
    plt.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Proportions of ALPHA and BETA')
    plt.show()

# Run the visualization
if __name__ == "__main__":
    plot_alpha_beta()
