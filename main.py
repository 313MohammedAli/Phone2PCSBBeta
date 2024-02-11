from multiprocessing import Process, Manager

def run_server(q):
    import server  # Assuming server.py is refactored to a module
    server.main(q)  # main is a new function in server.py that takes a queue




def run_gui(q):
    import gui  # Assuming gui.py is refactored to a module
    gui.main(q)  # main is a new function in gui.py that takes a queue 

#Test


if __name__ == "__main__":
    with Manager() as manager:
        q = manager.Queue()

        server_process = Process(target=run_server, args=(q,))
        gui_process = Process(target=run_gui, args=(q,))

        server_process.start()
        gui_process.start()

        server_process.join()
        gui_process.join()
