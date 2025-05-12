import pickle

class Customer:
    def __init__(self, id, name, email, phone):
        self.__id = id
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__purchase_history = []

    # Hardcore getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    # Minimal setters
    def set_name(self, new_name):
        self.__name = new_name

    def set_email(self, new_email):
        self.__email = new_email

    def set_phone(self, new_phone):
        self.__phone = new_phone

    # purchase methods
    def add_purchase(self, ticket):
        '''
        Takes the ticket and adds the ticket into the purchased tickets list
        :param ticket:
        :return:
        '''
        self.__purchase_history.append(ticket)

    def cancel_purchase(self, ticket):
        '''
        This method cancels the purchase by removing the ticket from the list
        :param ticket:
        :return:
        '''
        self.__purchase_history.remove(ticket)

    def save_to_file(self):
        '''
        This method adds the customer information into the binary pickle file
        from which the information can be read whenever required.
        :return:
        '''
        try:
            with open("customers.pkl", "rb") as file:
                customers = pickle.load(file)
        except (FileNotFoundError, EOFError):
            customers = []

        customers.append(self)

        with open("customers.pkl", "wb") as file:
            pickle.dump(customers, file)

    def __str__(self):
        return "*** Showing Details for Customer ***\nID : {}\nName : {}\n" \
               "Email : {}\nPhone : {}\nTotal Orders : {}".format(self.get_id(),self.get_name(),
                                                                  self.get_email(),self.get_phone(),
                                                                  len(self.__purchase_history))




class Ticket:
    def __init__(self, price):
        self.__price = price
        self.__is_valid = True

    def get_price(self):
        return self.__price

    def is_valid(self):
        return self.__is_valid

    def set_price(self, new_price):
        self.__price = new_price

    def invalidate(self):
        self.__is_valid = False

    def get_ticket_type(self):
        pass

class SingleRaceTicket(Ticket):
    def __init__(self, price, seat_number):
        super().__init__(price)
        self.__seat_number = seat_number

    def get_seat_number(self):
        return self.__seat_number

    def get_ticket_type(self):
        return "SINGLE_RACE"

class WeekendPackageTicket(Ticket):
    def __init__(self, price, seat_number):
        super().__init__(price)
        self.__seat_number = seat_number

    def get_seat_number(self):
        return self.__seat_number

    def get_ticket_type(self):
        return "WEEKEND_PACKAGE"

class SeasonMembershipTicket(Ticket):
    def __init__(self, price, seat_number):
        super().__init__(price)
        self.__seat_number = seat_number

    def get_seat_number(self):
        return self.__seat_number

    def get_ticket_type(self):
        return "SEASON_MEMBERSHIP"
