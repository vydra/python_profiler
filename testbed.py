#!/usr/bin/env python3
"""
Testbed for demonstrating the Profiler class functionality.
This script shows how to use the Profiler to measure execution times
of different code segments across multiple iterations.
"""

import time
import random
from profiler import Profiler

def simulate_work(min_ms=10, max_ms=100):
    """Simulate work by sleeping for a random amount of time."""
    sleep_time = random.uniform(min_ms, max_ms) / 1000  # Convert to seconds
    time.sleep(sleep_time)
    return sleep_time * 1000  # Return actual sleep time in ms

def main():
    # Create a profiler instance
    profiler = Profiler()
    
    print("Running profiler test with multiple iterations and segments...")
    
    # Run 5 iterations
    for i in range(1, 6):
        iteration = profiler.start_iteration()
        print(f"\nIteration {iteration}:")
        
        # Segment A
        start_time = time.time() * 1000  # Convert to ms
        work_time = simulate_work(50, 150)
        end_time = time.time() * 1000
        profiler.record("Segment A", start_time, end_time, iteration)
        print(f"  Segment A completed in {end_time - start_time:.2f}ms (simulated: {work_time:.2f}ms)")
        
        # Segment B (run multiple times per iteration)
        for j in range(3):
            start_time = time.time() * 1000
            work_time = simulate_work(10, 50)
            end_time = time.time() * 1000
            profiler.record("Segment B", start_time, end_time, iteration)
            print(f"  Segment B (run {j+1}) completed in {end_time - start_time:.2f}ms (simulated: {work_time:.2f}ms)")
        
        # Segment C
        start_time = time.time() * 1000
        work_time = simulate_work(30, 80)
        end_time = time.time() * 1000
        profiler.record("Segment C", start_time, end_time, iteration)
        print(f"  Segment C completed in {end_time - start_time:.2f}ms (simulated: {work_time:.2f}ms)")
    
    # Print profiling results
    print("\n--- Profiling Results ---")
    print(f"Total number of executions: {profiler.numberOfExecutions()}")
    print(f"Segments measured: {profiler.listSegments()}")
    
    # Print average durations for each segment
    print("\nAverage durations across all iterations:")
    for segment in profiler.listSegments():
        avg = profiler.averageDuration(segment)
        print(f"  {segment}: {avg:.2f}ms")
    
    # Print data for a specific iteration
    iteration_to_show = 3
    print(f"\nDetailed data for iteration {iteration_to_show}:")
    iteration_data = profiler.iterationData(iteration_to_show)
    for record in iteration_data:
        print(f"  {record['segment_name']}: {record['duration']:.2f}ms")
    
    # Show average of Segment B for each iteration
    print("\nAverage duration of Segment B for each iteration:")
    for i in range(1, 6):
        avg = profiler.averageDuration("Segment B", i)
        print(f"  Iteration {i}: {avg:.2f}ms")

if __name__ == "__main__":
    main()
