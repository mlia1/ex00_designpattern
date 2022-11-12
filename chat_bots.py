from time import sleep, perf_counter #profiling delle operazioni : voglio vedere quanto tempo impiega
import threading
from sys import exit
#florp e zorp sono due entità che bogliono diventare chatbots
sentence_mutex= threading.Lock()
    
class ChatBot:
    def __init__(self, name, tutor) -> None:
        self.worker=threading.Thread(target=self.speak, name=name)
        self.counter=0
        self.tutor=tutor
        pass

    def start_speaking(self):
        self.worker.start()
    
    def wait(self):
        self.worker.join()

    def speak_internal(self):
        pass

    def speak(self):
        print(threading.get_ident())
        for self.counter in range(0,10):
            print("Thread id: ",threading.current_thread().name)
            self.speak_internal()
            self.tutor.observe(self.counter)
            sleep(0.08)

class Florp(ChatBot):
    def __init__(self, name, tutor) ->None:
        super().__init__(name, tutor)
    
    def speak_internal(self):
        print("blip florp")

class Zorp(ChatBot):
    def __init__(self, name, tutor) ->None:
        super().__init__(name, tutor)

    def speak_internal(self):
        print("blip zorp")
# voglio introdurre dei design pattern
# scrivo un builder
class StudentBuilder:
    def __init__(self) -> None:
        pass
    def build(name, tutor):
        if name == "zorp":
            return Zorp(name=name, tutor=tutor)
        elif name == "florp":
            return Florp(name=name, tutor=tutor)
        else :
            return ChatBot("")

class Trainer:
    def __init__(self) -> None:
        self.students=[]
    def accept_student(self, student):
        self.students.append(student)
    def train_student(self):
        for student in self.students:
            student.start_speaking()

#introduco il tutor che osserva
class Tutor:
    def __init__(self, notify_function) -> None:
        self.notify=notify_function
    def observe(self, num):
        if num == 5:
            self.notify()

def notification():
    print("training half complete")


def main():
    print("Training session beginning")
    tutor=Tutor(notify_function=notification)
    trainer=Trainer()
    trainer.accept_student(StudentBuilder.build(name ="florp", tutor=tutor))
    trainer.accept_student(StudentBuilder.build(name ="zorp", tutor=tutor))

    trainer.train_student()

if __name__=="__main__":
    start_time = perf_counter()
    main() #main thread
    stop_time = perf_counter()
    print(f"It took {(stop_time - start_time)*1000 : 0.2f} milliseconds (s) to complete")
