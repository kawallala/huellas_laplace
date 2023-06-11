from whatsapp_api_client_python import API as API


class WhatsappService:
    def __init__(self) -> None:
        self.greenAPI = API.GreenApi(
            "1101830048", "b2cfa75f397149158bc52aef3f8b6f9d7d7f3f11dc194b83a6"
        )

    def send_message(self, number, message):
        # send message using green api to the number +56987339658
        result = self.greenAPI.sending.sendMessage(number[1:]+"@c.us", message)
        print(result)
        return result
