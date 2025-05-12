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


class RacingCarEvent:
    def __init__(self, name, location, date, capacity):
        self.__name = name
        self.__location = location
        self.__date = date
        self.__capacity = capacity
        self.__total_sales = 0
        self.__tickets_sold = []  # List of Ticket objects
        self.__registered_customers = []
        self.__discount_policy = None

    # Getters
    def get_name(self):
        return self.__name

    def get_location(self):
        return self.__location

    def get_date(self):
        return self.__date

    def get_capacity(self):
        return self.__capacity

    def get_total_sales(self):
        return self.__total_sales

    def get_total_tickets_sold(self):
        return len(self.__tickets_sold)

    def get_discount_policy(self):
        return self.__discount_policy

    # Setters
    def set_name(self, new_name):
        self.__name = new_name

    def set_location(self, new_location):
        self.__location = new_location

    def set_date(self, new_date):
        self.__date = new_date

    def set_discount_policy(self,policy):
        self.__discount_policy = policy

    # Admin methods

    def get_customer_by_id(self,id):
        '''
        This method takes the id and returns the customer if the id matches.
        otherwise it returns false.
        :param id: 
        :return: 
        '''
        for customer in self.__registered_customers:
            if id == customer.get_id():
                return customer

        return False

    def register_customer(self,customer):
        '''
        This method registers a customer.
        :param customer: 
        :return: 
        '''
        self.__registered_customers.append(customer)

    def unregister_customer(self,customer):
        '''
        This methos unregisters a customer and removes it from the list.
        :param customer: 
        :return: 
        '''
        self.__registered_customers.remove(customer)

    def add_ticket_sale(self,ticket):
        '''
        This method adds the ticket and adds its price into the sales of the event.
        :param ticket: 
        :return: 
        '''
        if self.get_discount_policy().is_discount_active():
            price_after_discount = self.get_discount_policy().apply_discount(ticket.get_price())

            self.__total_sales += price_after_discount
            self.__tickets_sold.append(ticket)
        else:
            self.__total_sales += ticket.get_price()
            self.__tickets_sold.append(ticket)


    def get_total_customers(self):
        '''
        This returns the number of total registered customers
        :return: 
        '''
        return len(self.__registered_customers)


class DiscountPolicy:
    def __init__(self, discount_pct, policy_state):
        self.__discount_active = policy_state
        self.__discount_percentage = discount_pct

    def enable_discount(self):
        self.__discount_active = True

    def disable_discount(self):
        self.__discount_active = False

    def is_discount_active(self):
        return self.__discount_active

    def apply_discount(self, original_price):
        """
        Apply discount to the original price if policy is active
        Returns discounted price or original price
        """
        if self.__discount_active:
            return original_price * (1 - self.__discount_percentage / 100)
        return original_price

    def get_policy_details(self):
        if self.__discount_active:
            return f"{self.__discount_percentage}% discount"
        return "No discount"

# creating data storage files functions
def create_customers_file():
    with open("customers.pkl", "wb") as file:
        pickle.dump([], file)


def create_tickets_file():
    with open("tickets.pkl", "wb") as file:
        pickle.dump([], file)


# creating the files
create_customers_file()
create_tickets_file()

# creating the event object
event = RacingCarEvent("Racing Car Event","UAE","05/09/2025",300)
policy = DiscountPolicy(10,True)

# assigning the discount policy
event.set_discount_policy(policy)

# creating customer objects
c4 = Customer("4","Zayed","zayed@gmail.com","123456789")
c5 = Customer("5","Ahmed","ahmed@gmail.com","123456789")
c6 = Customer("6","Umar","umer@gmail.com","123456789")

# registering the customers
event.register_customer(c4)
event.register_customer(c5)
event.register_customer(c6)

