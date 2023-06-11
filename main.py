import serialService
import persona_repo
import applicationController
import gui


if __name__ == "__main__":
    reader = serialService.SerialReader()
    repo = persona_repo.PersonRepository()
    controller = applicationController.applicationController(reader, repo)
    app = gui.App(controller)
    app.mainloop()
