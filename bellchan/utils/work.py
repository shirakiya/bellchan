from multiprocessing import Process


def parallel(job_function):
    job_process = Process(target=job_function)
    job_process.start()
