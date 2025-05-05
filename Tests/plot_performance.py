import matplotlib.pyplot as plt

# Simulated data (replace with your actual Locust test results)
concurrent_users = [1, 5, 10, 15, 20]
response_times = [1.2, 2.5, 3.5, 4.8, 6.0]  # Average response times in seconds

plt.figure(figsize=(8, 6))
plt.plot(concurrent_users, response_times, marker='o', color='b', label='Response Time (s)')
plt.title('Concurrent Users vs. Response Time')
plt.xlabel('Number of Concurrent Users')
plt.ylabel('Response Time (seconds)')
plt.grid(True)
plt.legend()

plt.savefig('performance_graph.png')