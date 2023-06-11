import serial_service
import persona_repo
import applicationController
import gui


if __name__ == "__main__":
    reader = serial_service.SerialReader()
    repo = persona_repo.PersonRepository()
    controller = applicationController.applicationController(reader, repo)
    app = gui.App(controller)
    app.mainloop()
