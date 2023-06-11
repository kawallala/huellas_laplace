from whatsapp_api_client_python import API as API


class WhatsappService:
    def __init__(self) -> None:
        self.greenAPI = API.GreenApi(
            "1101826297", "0b168357f7694566a8a4f716ec766f1f189fc8920c6c43cfb1"
        )

    def send_message(self, number, message):
        # send message using green api to the number +56987339658
        result = self.greenAPI.sending.sendMessage(number, message)
        return result
