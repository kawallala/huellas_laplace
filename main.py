import serial_service
import persona_repo
import applicationController
import logs_service
import gui


if __name__ == "__main__":
    [app_logger, person_logger] = logs_service.create_logs()
    reader = serial_service.SerialReader(app_logger)
    repo = persona_repo.PersonRepository(app_logger)
    controller = applicationController.applicationController(reader, repo, app_logger, person_logger)
    app = gui.App(controller)
    app.mainloop()
