"""
=============================================================================
Assignment: Python Concurrency & Async Execution
Instructions: Review the task requirements and objectives listed below.
=============================================================================
"""

# =============================================================================
# Task 1: Pure Synchronous Execution
# =============================================================================
"""
Objective: Understand execution blocking in synchronous programs.

Requirements:
- Create a function called: run_sync_tasks()
- Execute 8 tasks using: time.sleep()
- Each task must print: Start -> delay -> Finish
- Calculate the total execution time
- Each task starts only after the previous one finishes
- Execution is fully sequential
"""
import time
def sync_task(task_id):
    print(f"Task {task_id} → Start")

    time.sleep(1)

    print(f"Task {task_id} → Finish")


def run_sync_tasks():

    print("=" * 50)
    print("TASK 1 — PURE SYNCHRONOUS EXECUTION")
    print("=" * 50)

    start_time = time.perf_counter()

    # Execute 8 tasks sequentially
    for i in range(1, 9):
        sync_task(i)

    end_time = time.perf_counter()

    total_time = end_time - start_time

    print("=" * 50)
    print(f"Total execution time: {total_time:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    run_sync_tasks()

# =============================================================================
# Task 2: Async Sequential (Without gather)
# =============================================================================
"""
Objective: Understand that async does NOT automatically mean parallel.

Requirements:
- Use async functions
- Create an async task function
- Call tasks like this: await task() inside a loop
- Execution remains sequential
- Total execution time is similar to synchronous execution
"""
#TASK 2 — ASYNC SEQUENTIAL
import asyncio
import time


async def async_task(task_id):
    print(f"Task {task_id} → Start")
    await asyncio.sleep(1)
    print(f"Task {task_id} → Finish")


async def run_async_sequential():
    print("=" * 50)
    print("TASK 2 — ASYNC SEQUENTIAL")
    print("=" * 50)

    start_time = time.perf_counter()

    for i in range(1, 9):
        await async_task(i)

    end_time = time.perf_counter()

    print("=" * 50)
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(run_async_sequential())
# =============================================================================
# Task 3: Async Concurrent Using gather()
# =============================================================================
"""
Objective: Understand real concurrency using asyncio.

Requirements:
- Create a list of tasks
- Use: await asyncio.gather(...) to execute them
- All tasks start almost at the same time
- Execution time becomes significantly shorter
"""
import asyncio
import time


async def async_task(task_id):
    print(f"Task {task_id} → Start")
    await asyncio.sleep(1)
    print(f"Task {task_id} → Finish")


async def run_async_concurrent():
    print("=" * 60)
    print("TASK 3 — ASYNC CONCURRENT USING GATHER")
    print("=" * 60)

    start_time = time.perf_counter()

    tasks = [
        async_task(i)
        for i in range(1, 9)
    ]

    await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    print("=" * 60)
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_async_concurrent())
# =============================================================================
# Task 4: Blocking CPU Inside Event Loop
# =============================================================================
"""
Objective: Understand why CPU-bound operations break async workflows.

Requirements:
- Create a function called: heavy_cpu_function() that contains a large loop or heavy computation
- Run it directly inside an async main function
- Other async tasks stop running
- Event loop becomes blocked
"""
import asyncio
import time


def heavy_cpu_function():
    total = 0

    for i in range(20_000_000):
        total += i * i

    return total


async def light_async_task():
    for i in range(5):
        print(f"Light async task → {i + 1}")
        await asyncio.sleep(0.5)


async def run_blocking_cpu():
    print("=" * 60)
    print("TASK 4 — BLOCKING CPU INSIDE EVENT LOOP")
    print("=" * 60)

    start_time = time.perf_counter()

    light_task = asyncio.create_task(
        light_async_task()
    )

    print("\nStarting heavy CPU function...")

    # Blocking CPU work inside event loop
    result = heavy_cpu_function()

    print("Heavy CPU function finished.")

    await light_task

    end_time = time.perf_counter()

    print("\nCPU result:", result)
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_blocking_cpu())
# =============================================================================
# Task 5: Yielding Inside Single Thread
# =============================================================================
"""
Objective: Understand cooperative multitasking.

Requirements:
- Inside a loop use: await asyncio.sleep(0)
- Event loop can switch between tasks
- Improved responsiveness
"""
import asyncio
import time


async def yielding_task(task_id):
    for i in range(5):
        print(f"Task {task_id} → iteration {i + 1}")

        # Yield control to the event loop
        await asyncio.sleep(0)


async def run_yielding_tasks():
    print("=" * 60)
    print("TASK 5 — YIELDING WITH asyncio.sleep(0)")
    print("=" * 60)

    start_time = time.perf_counter()

    task1 = asyncio.create_task(
        yielding_task(1)
    )

    task2 = asyncio.create_task(
        yielding_task(2)
    )

    task3 = asyncio.create_task(
        yielding_task(3)
    )

    await asyncio.gather(
        task1,
        task2,
        task3
    )

    end_time = time.perf_counter()

    print("=" * 60)
    print(f"Total execution time: {end_time - start_time:.4f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_yielding_tasks())
# =============================================================================
# Task 6: Using asyncio.to_thread()
# =============================================================================
"""
Objective: Solve blocking issues using threads.

Requirements:
- Run the heavy CPU function using: await asyncio.to_thread(...)
- Light async tasks continue running smoothly
- Event loop remains responsive
"""
import asyncio
import time


def heavy_cpu_function():
    total = 0

    for i in range(20_000_000):
        total += i * i

    return total


async def light_async_task():
    for i in range(5):
        print(f"Light async task → {i + 1}")
        await asyncio.sleep(0.5)


async def run_to_thread():
    print("=" * 60)
    print("TASK 6 — asyncio.to_thread()")
    print("=" * 60)

    start_time = time.perf_counter()

    print("\nStarting CPU work in a separate thread...")

    cpu_task = asyncio.create_task(
        asyncio.to_thread(
            heavy_cpu_function
        )
    )

    light_task = asyncio.create_task(
        light_async_task()
    )

    result = await cpu_task

    print("\nHeavy CPU function finished.")

    await light_task

    end_time = time.perf_counter()

    print("\nCPU result:", result)
    print(f"Total execution time: {end_time - start_time:.2f} seconds")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(run_to_thread())

# =============================================================================
# Task 7: Race Condition Simulation
# =============================================================================
"""
Objective: Understand thread synchronization and race conditions.

Requirements:
- Create a shared variable: shared counter = 0
- Run multiple threads modifying it
- Execute twice:
  * Without Lock
  * Using: threading.Lock()
- Different results between both cases
- Race condition problems without synchronization
"""
import time
import threading


shared_counter = 0


def increment_without_lock(iterations):
    global shared_counter

    for _ in range(iterations):

        current_value = shared_counter

        # Increase chance of race condition
        time.sleep(0.000001)

        shared_counter = current_value + 1


def run_without_lock():
    global shared_counter

    print("=" * 60)
    print("TASK 7 — WITHOUT LOCK")
    print("=" * 60)

    shared_counter = 0

    threads = []

    number_of_threads = 10
    iterations_per_thread = 1000

    for _ in range(number_of_threads):

        thread = threading.Thread(
            target=increment_without_lock,
            args=(iterations_per_thread,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    expected = number_of_threads * iterations_per_thread

    print(f"Expected counter: {expected}")
    print(f"Actual counter:   {shared_counter}")


counter_lock = threading.Lock()


def increment_with_lock(iterations):
    global shared_counter

    for _ in range(iterations):

        with counter_lock:

            current_value = shared_counter

            time.sleep(0.000001)

            shared_counter = current_value + 1


def run_with_lock():
    global shared_counter

    print("\n" + "=" * 60)
    print("TASK 7 — WITH LOCK")
    print("=" * 60)

    shared_counter = 0

    threads = []

    number_of_threads = 10
    iterations_per_thread = 1000

    for _ in range(number_of_threads):

        thread = threading.Thread(
            target=increment_with_lock,
            args=(iterations_per_thread,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    expected = number_of_threads * iterations_per_thread

    print(f"Expected counter: {expected}")
    print(f"Actual counter:   {shared_counter}")


if __name__ == "__main__":

    run_without_lock()

    run_with_lock()
# =============================================================================
# Task 8: Async + Thread Synchronization Hybrid
# =============================================================================
"""
Objective: Combine async workflows with threads and synchronization.

Requirements:
- Async tasks should request CPU work
- CPU work must run inside a thread
- Thread modifies a shared variable protected by Lock
- Async orchestration with thread safety
- Parallel execution without data corruption
"""
import asyncio
import time
import threading


hybrid_counter = 0

hybrid_lock = threading.Lock()


def hybrid_cpu_work(task_id, iterations=1_000_000):

    total = 0

    # CPU-intensive work
    for i in range(iterations):
        total += i * i

    # Safely update shared variable
    global hybrid_counter

    with hybrid_lock:
        hybrid_counter += 1
        current_counter = hybrid_counter

    return task_id, total, current_counter


async def async_cpu_request(task_id):

    print(
        f"Async Task {task_id} → "
        f"Requesting CPU work..."
    )

    # Run CPU work inside a separate thread
    task_id, result, counter_value = await asyncio.to_thread(
        hybrid_cpu_work,
        task_id
    )

    print(
        f"Async Task {task_id} → "
        f"Finished | Shared Counter = {counter_value}"
    )

    return result


async def run_hybrid():

    global hybrid_counter

    print("=" * 70)
    print("TASK 8 — ASYNC + THREAD SYNCHRONIZATION HYBRID")
    print("=" * 70)

    hybrid_counter = 0

    start_time = time.perf_counter()

    tasks = [
        async_cpu_request(i)
        for i in range(1, 9)
    ]

    results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print("Expected shared counter: 8")
    print(f"Actual shared counter:   {hybrid_counter}")
    print(f"Number of results:        {len(results)}")

    print(
        f"Total execution time:     "
        f"{end_time - start_time:.2f} seconds"
    )

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_hybrid())






