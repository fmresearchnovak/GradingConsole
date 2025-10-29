import matplotlib.pyplot as plt



def calculate_stats(numbers):
    # Sort the data for median calculation
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)

    # Min and Max
    min_val = sorted_numbers[0]
    max_val = sorted_numbers[-1]

    # Mean
    mean_val = sum(numbers) / n

    # Median
    if n % 2 == 1:
        # Odd number of elements, median is the middle element
        median_val = sorted_numbers[n // 2]
    else:
        # Even number of elements, median is the average of the two middle elements
        mid1 = sorted_numbers[n // 2 - 1]
        mid2 = sorted_numbers[n // 2]
        median_val = (mid1 + mid2) / 2

    return min_val, mean_val, median_val, max_val
    
    
def main():
    
    data = [26, 37, 42, 45, 34, 44, 40, 35.5, 42, 46.5, 37, 42, 32, 44, 32, 31]
    data = [int((x / 53.0) * 100) for x in data] # turn into percentages

    min_val, mean_val, median_val, max_val = calculate_stats(data)

    # Format the statistics for display
    stats_text = (
        f"Min: {min_val}%\n"
        f"Median: {median_val:.2f}%\n"
        f"Mean: {mean_val:.2f}%\n"
        f"Max: {max_val}%"
    )

    # --- 2. Plotting the Histogram ---

    # Create the figure and axes
    fig, ax = plt.subplots()#figsize=(16, 9))

    # Plot the histogram
    ax.hist(data, bins='auto', range=(0, 100), edgecolor='black')

    # Add the statistics text to the top-left corner
    # 'transform=ax.transAxes' places the coordinates relative to the axes (0,0 is bottom-left, 1,1 is top-right)
    ax.text(
        0.05,        # x-coordinate (5% from the left edge)
        0.95,        # y-coordinate (95% from the bottom edge)
        stats_text,
        transform=ax.transAxes,
        fontsize=11,
        verticalalignment='top',
        bbox=dict(boxstyle="round,pad=0.5", facecolor='white', alpha=0.8, edgecolor='gray')
    )

    # Set titles and labels
    ax.set_title('Grade Histogram', fontsize=16)
    ax.set_xlabel('Grade (%)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    #ax.grid(axis='y', alpha=0.5)
    
    plt.savefig("grade_distribution.png")

    # Display the plot
    plt.show()
    

    
main()
