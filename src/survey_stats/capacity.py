import multiprocessing

def number_of_proles():
    return int(multiprocessing.cpu_count() - 2)

def number_of_workers():
    return int(multiprocessing.cpu_count()/2.0)


