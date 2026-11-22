
class Hotel:
    """
    This is a class as hotel management system, managing the booking,
    check-in, check-out, and availability of rooms in a hotel
    with different room types.
    """

    def __init__(self, name, rooms):
        """
        Initialize the hotel management system.
        """
        self.name = name
        self.available_rooms = rooms
        self.booked_rooms = {}

    def book_room(self, room_type, room_number, name):
        """
        Book rooms of the specified type for a guest.
        """
        if room_type not in self.available_rooms:
            return False

        available = self.available_rooms[room_type]

        if room_number > available:
            if available == 0:
                return False
            return available

        if room_number <= 0:
            return False

        self.available_rooms[room_type] -= room_number

        if room_type not in self.booked_rooms:
            self.booked_rooms[room_type] = {}

        if name not in self.booked_rooms[room_type]:
            self.booked_rooms[room_type][name] = 0

        self.booked_rooms[room_type][name] += room_number

        return 'Success!'

    def check_in(self, room_type, room_number, name):
        """
        Check in a guest with an existing booking.
        """
        if room_type not in self.booked_rooms:
            return False

        if name not in self.booked_rooms[room_type]:
            return False

        booked_quantity = self.booked_rooms[room_type][name]

        if room_number <= 0 or room_number > booked_quantity:
            return False

        if room_number == booked_quantity:
            del self.booked_rooms[room_type][name]
        else:
            self.booked_rooms[room_type][name] -= room_number

    def check_out(self, room_type, room_number):
        """
        Check out rooms and update availability.
        """
        if room_type not in self.available_rooms:
            self.available_rooms[room_type] = 0

        self.available_rooms[room_type] += room_number

    def get_available_rooms(self, room_type):
        """
        Return the number of available rooms of a specified type.
        """
        return self.available_rooms.get(room_type, 0)
