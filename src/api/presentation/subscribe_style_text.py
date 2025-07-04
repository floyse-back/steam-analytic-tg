




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
        return (
            "<b>✔️ Успішно:</b> <i>підписку активовано.</i>"
        )

    def after_unsubscribe(self):
        return (
            "<b>🛑 Підписку скасовано.</b> <i>Ви більше не отримуватимете оновлення з цієї категорії.</i>"
        )

    def after_bad_subscribe(self):
        return (
            "<b>⚠️ Неможливо оформити підписку.</b> <i>Ймовірно, вона вже активна або виникла помилка.</i>"
        )

    def after_bad_unsubscribe(self):
        return (
            "<b>⚠️ Скасування не виконано.</b> <i>Підписка, можливо, вже була скасована або не існувала.</i>"
        )
