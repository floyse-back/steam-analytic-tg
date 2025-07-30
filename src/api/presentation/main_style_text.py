


class MainStyleText:
    @classmethod
    def subscribe_channel(cls,channel_url):
        return (
        "❗ <b>Щоб користуватись ботом, потрібно підписатись на наш канал</b>\n\n"
        f"📢 <a href='{channel_url}'>Підписатись на канал</a>\n\n"
        "Після підписки натисни кнопку нижче 👇"
    )

    def start_message_no_steam_id(self,username):
        return (f"👋 <b>Привіт, радий тебе бачити, @{username}!</b>\n"
                         f"🎮 <b>Щоб продовжити, надішли свій Steam профіль:</b>\n"
                         f"• 🔢 SteamID64 (наприклад: <code>7656119...</code>)\n"
                         f"• ✏️ Нік з URL (наприклад: <code>floysefake</code>)\n"
                         f"• 🔗 Посилання на профіль (будь-якого типу)\n\n"
                         f"<i>Ми автоматично все розпізнаємо 😉</i>")

    def start_message_with_steam_id(self,username):
        return (f"<b>Привіт, радий тебе знову бачити, @{username}!</b>\n")