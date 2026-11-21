   hotel.book_room('single', 1) → 'Success!'


   hotel.book_room('single', 5) → 4


   hotel.book_room('single', 4) → 'Success!'


   hotel.book_room('single', 6) → 0


def book_room(self, room_type, room_number):
    if room_type not in self.available_rooms:
        return False

    available = self.available_rooms[room_type]
    if room_number <= available:
        return 'Success!'
    else:
        return available - room_number


self.available_rooms = {'single': 6}
