""" Model for aircraft flights """


class Flight:
    """A flight with a particular passanger aircraft"""

    def __init__(self, number, aircraft):
        if not number[:2].isalpha():
            raise ValueError("No airline code in {}".format(format(number)))

        if not number[:2].isupper():
            raise ValueError("Invalid airline code {}".format(number))

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number {}".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]


    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def _parse_seat(self, seat):
        """Parse a seat designator into a valid row and letter.

        Args.
            seat: A seat designator such as '12F'

        Returns:
            A tuple containing an integer and a string for row and seat.
        """

        row_numbers, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter {}".format(letter))

        row_text = seat[:-1]

        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row {}".format(row_text))


        if row not in row_numbers:
            raise ValueError("Invalid row number {}".format(row))

        return row, letter

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                   for row in self._seating
                   if row is not None)


    def make_boarding_cards(self, card_printer):
        for passanger, seat in sorted(self._passanger_seats()):
            card_printer(passanger, seat, self._number, self._aircraft.model())


    def _passanger_seats(self):
        """An iterable series of passanger seating allocations"""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passanger = self._seating[row][letter]
                if passanger is not None:
                    yield (passanger, "{}{}".format(row, letter))


    def allocate_seat(self, seat, passanger):
        """Allocate a seat to a passanger

        Args:
            seat: A seat designator such as '12C' or '21F'
            passanger: The passanger name.

        Raises:
            ValueError: If the seat is unavailable.
        """

        row, letter = self._parse_seat(seat)

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied".format(seat))

        self._seating[row][letter] = passanger


    def rellocate_passanger(self, from_seat, to_seat):
        """Relocate a passanger to a different seat

        Args:
            from_seat: The existing seat designator for the passanger to be
            moved

            to_seat: The new seat designator
        """
        from_row, from_letter = self._parse_seat(from_seat)
        to_row, to_letter = self._parse_seat(to_seat)

        if self._seating[from_row][from_letter] is None:
            raise ValueError("No passanger to relocate in seat {}".format(from_seat))

        if self._seating[to_row][to_letter] is not None:
            raise ValueError("Seat {} already occupied".format(to_seat))


        self._seating[to_row][to_letter] = self._seating[from_row][from_letter]
        self._seating[from_row][from_letter] = None

# class Aircraft:
#
#     def __init__(self, registration, model, num_rows, num_seats_per_row):
#         self._registration = registration
#         self._model = model
#         self._num_rows = num_rows
#         self._num_seats_per_row = num_seats_per_row
#
#
#     def registration(self):
#         return self._registration
#
#
#     def model(selfs):
#         return  selfs._model
#
#
#     def seating_plan(self):
#         return (range(1, self._num_rows + 1), "ABCDEFJHIJK"[:self._num_seats_per_row])

class Aircraft:

    def __init__(self, registration):
        self._registration = registration

    def registration(self):
        return self._registration

    def num_seats(self):
        rows, rows_seats = self.seating_plan()
        return len(rows) * len(rows_seats)


class AirbusA319(Aircraft):

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"

class Boing777(Aircraft):

    def model(self):
        return "Boing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHIJK"


def make_flight():
    # f = Flight("AZ610", Aircraft("G-EUPT", "Airbus A310", num_rows=22, num_seats_per_row=6))
    # f.allocate_seat("12A", "Guido Paniguara")
    # f.allocate_seat("1A", "Benajamin Bottom")
    # f.allocate_seat("15F", "Benajmin Frankling")
    # f.allocate_seat("1C", "Rodrigo Franco")
    # f.allocate_seat("1D", "Andres casinelli")

    i = Flight("PE979", Boing777("P-LATA"))
    i.allocate_seat("1A", "Marvin Abisrror")
    i.allocate_seat("2C", "Perla Cristal")
    i.allocate_seat("20A", "Carla Segovia")
    i.allocate_seat("15B", "Cintia Irina")
    i.allocate_seat("12B", "Esmeralda Princesa")

    g = Flight("BA758", AirbusA319("G-EUPT"))
    g.allocate_seat("12A","Alejandro Perez")
    g.allocate_seat("15F", "Armando Paredes")
    g.allocate_seat("12B", "Ciro Perez")
    g.allocate_seat("1A", "Peredo marco")
    g.allocate_seat("3C", "Gilberto tuesta")


    return i, g

def console_card_printer(passanger, seat, flight_number, aircraft):
    output = "| Name: {0}"        \
             "  Flight: {1}"      \
             "  Seat: {2}"        \
             "  Aircraft: {3}"    \
             " |".format(passanger, flight_number, seat, aircraft)

    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + " " * (len(output) - 2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()
