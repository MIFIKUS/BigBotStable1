import time

for i in range(10):
    print(f"Прогресс: {i}%", end="\r")
    time.sleep(1)
