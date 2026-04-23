class ChatManager:
    def __init__(self):
        self.queue = []
        self.active_chats = {}

    def is_in_chat(self, user_id: int) -> bool:
        return user_id in self.active_chats

    def is_in_queue(self, user_id: int) -> bool:
        return user_id in self.queue

    def add_to_queue(self, user_id: int):
        if not self.is_in_queue(user_id):
            self.queue.append(user_id)

    def try_create_chat(self, user_id: int):
        if self.queue:
            partner_id = self.queue.pop(0)
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