class ChatManager:
    def __init__(self):
        self.queue = []
        self.active_chats = {}
        self.blacklist = set()

    def is_in_chat(self, user_id: int) -> bool:
        return user_id in self.active_chats

    def is_in_queue(self, user_id: int) -> bool:
        return user_id in self.queue

    def is_banned(self, user_id: int) -> bool:
        return user_id in self.blacklist

    def ban_user(self, user_id: int):
        self.blacklist.add(user_id)

    def add_to_queue(self, user_id: int):
        if self.is_banned(user_id):
            return False
        if not self.is_in_queue(user_id):
            self.queue.append(user_id)
            return True
        return False

    def try_create_chat(self, user_id: int):
        if self.is_banned(user_id):
            return "banned"

        if self.queue:
            partner_id = self.queue.pop(0)

            if self.is_banned(partner_id):
                return self.try_create_chat(user_id)

            self.active_chats[user_id] = partner_id
            self.active_chats[partner_id] = user_id
            return partner_id

        self.add_to_queue(user_id)
        return None

    def end_chat(self, user_id: int):
        if self.is_in_chat(user_id):
            partner_id = self.active_chats.pop(user_id)
            self.active_chats.pop(partner_id, None)
            return partner_id
        return None

    def get_partner(self, user_id: int):
        return self.active_chats.get(user_id)