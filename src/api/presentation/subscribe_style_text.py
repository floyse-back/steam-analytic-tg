




class SubscribeStyleText:
    def user_have_subscribe(self, description: str):
        return (
            f"{description}\n\n"
            f"✅ <b>Ви вже підписані на цю категорію.</b>"
        )

    def user_dont_have_subscribe(self, description: str):
        return (
            f"{description}\n\n"
            f"❗️ <b>Ви ще не підписані.</b>\n"
            f"Не зволікайте — підпишіться та отримуйте сповіщення першими! 😉"
        )

    def after_subscribes(self):
        return (f"✔️ <b>Операція пройшла успішно — підписка активна!</b>")

    def after_unsubscribe(self):
        return "🛑 Ви більше не отримуватимете оновлення цієї категорії."