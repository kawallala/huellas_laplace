import serialService
import personaRepo
import applicationController
import gui


if __name__ == "__main__":
    reader = serialService.SerialReader()
    repo = personaRepo.PersonRepository()
    controller = applicationController.applicationController(reader, repo)
    app = gui.App(controller)
    app.mainloop()
