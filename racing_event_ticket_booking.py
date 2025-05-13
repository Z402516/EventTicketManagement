
'''

Customer

Ticket (Abstract Base Class)

Subclasses: SingleRaceTicket, WeekendPackageTicket, SeasonMembershipTicket

RacingCarEvent

DiscountPolicy

PurchaseOrder

'''



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


single_race_ticket_price = 100
weekend_package_ticket_price = 200
season_membership_ticket_price = 1000
seat_number = 0


class TicketBookingApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Racing Event Ticket Booking System")
        self.root.geometry("850x500")
        self.root.resizable(False, False)

        # Create custom font
        heading_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
        section_font = tkfont.Font(family="Helvetica", size=12, weight="bold")

        # Main container frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Add the title above everything else
        title_label = tk.Label(
            self.main_frame,
            text="Racing Event Ticket Booking System",
            font=heading_font,
            fg="#333",
            bg="#d3d3d3",
            pady=10
        )
        title_label.pack(fill=tk.X)

        separator = tk.Frame(self.main_frame, height=2, bd=1, relief=tk.SUNKEN)
        separator.pack(fill=tk.X, pady=5)

        # Now create the content frames below the title
        content_frame = tk.Frame(self.main_frame)
        content_frame.pack(expand=True, fill=tk.BOTH)

        ## Account Management Frame
        # Left panel for account management
        left_frame = tk.Frame(content_frame, width=250, relief=tk.RIDGE, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=(0, 20))

        # Account management heading
        account_label = tk.Label(left_frame, text="Account Management", font=section_font)
        account_label.pack(pady=5, anchor=tk.W)

        # Add Customer button
        add_btn = tk.Button(left_frame, text="Add Customer", bg="#4caf50",command=self.open_add_customer_window)
        add_btn.pack(pady=5, fill=tk.X)

        # Delete Customer section
        del_frame = tk.Frame(left_frame)
        del_frame.pack(pady=5, fill=tk.X)

        tk.Button(del_frame, text="Delete Customer",command=self.delete_customer).pack(side=tk.LEFT)
        self.del_entry = tk.Entry(del_frame, width=15)
        self.del_entry.pack(side=tk.LEFT, padx=5)

        # Customer Details section
        details_frame = tk.Frame(left_frame)
        details_frame.pack(pady=5, fill=tk.X)

        tk.Button(details_frame, text="Customer Details",command=self.customer_details).pack(side=tk.LEFT)
        self.details_entry = tk.Entry(details_frame, width=15)
        self.details_entry.pack(side=tk.LEFT, padx=5)

        # Add a multi-line text area for output at the bottom
        output_label = tk.Label(left_frame, text="Output:", font=section_font)
        output_label.pack(pady=(10, 5), anchor=tk.W)

        # Create a container frame for Text + Scrollbar
        text_frame = tk.Frame(left_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Text widget
        self.output_text = tk.Text(
            text_frame,
            height=8,
            width=30,
            wrap=tk.WORD,
            state='normal',
            padx=5,
            pady=5
        )
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.output_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)



        ## New Ticket Booking Frame (middle panel)
        middle_frame = tk.Frame(content_frame, width=2000, relief=tk.RIDGE, borderwidth=2)
        middle_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=(0, 20))

        # Ticket Booking heading
        ticket_label = tk.Label(middle_frame, text="Ticket Booking", font=section_font)
        ticket_label.pack(pady=5, anchor=tk.W)

        # Ticket type dropdown
        tk.Label(middle_frame, text="Ticket Type:").pack(anchor=tk.W, padx=5, pady=(10, 0))
        self.ticket_type = tk.StringVar()
        ticket_options = ["Single-Race Passes", "Weekend Packages", "Season Ticket"]
        ticket_dropdown = tk.OptionMenu(middle_frame, self.ticket_type, *ticket_options)
        ticket_dropdown.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.ticket_type.set(ticket_options[0])  # Set default value

        # Payment method dropdown
        tk.Label(middle_frame, text="Payment Method:").pack(anchor=tk.W, padx=5)
        self.payment_method = tk.StringVar()
        payment_options = ["Credit Card", "Debit Card"]
        payment_dropdown = tk.OptionMenu(middle_frame, self.payment_method, *payment_options)
        payment_dropdown.pack(fill=tk.X, padx=5, pady=(0, 10))
        self.payment_method.set(payment_options[0])  # Set default value

        # Customer ID field
        tk.Label(middle_frame, text="Customer ID:").pack(anchor=tk.W, padx=5)

        self.customer_id_entry = tk.Entry(middle_frame,width=40)
        self.customer_id_entry.pack(fill=tk.X, padx=5, pady=(0, 15))

        # Book Ticket button
        book_btn = tk.Button(
            middle_frame,
            text="Book Ticket",
            command=self.book_ticket,  # You'll need to implement this method
            bg="#4caf50"
        )
        book_btn.pack(fill=tk.X, padx=5, pady=5)

        # Add output text area for booking messages
        booking_output_label = tk.Label(middle_frame, text="Booking Status:", font=section_font)
        booking_output_label.pack(pady=(10, 5), anchor=tk.W)

        # Create frame to hold text widget and scrollbar
        booking_text_frame = tk.Frame(middle_frame)
        booking_text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Text widget for booking output
        self.booking_output_text = tk.Text(
            booking_text_frame,
            height=8,
            width=20,
            wrap=tk.WORD,
            state='normal',
            padx=5,
            pady=5
        )
        self.booking_output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for booking output
        booking_scrollbar = tk.Scrollbar(booking_text_frame, command=self.booking_output_text.yview)
        booking_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.booking_output_text.config(yscrollcommand=booking_scrollbar.set)


        ## Admin Dashboard frame
        ## Admin Dashboard Frame (right panel)
        admin_frame = tk.Frame(content_frame, relief=tk.RIDGE, borderwidth=2)
        admin_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=(0, 20))

        # Admin Dashboard heading
        admin_label = tk.Label(admin_frame, text="Admin Dashboard", font=section_font)
        admin_label.pack(pady=5, anchor=tk.W)

        # Separator line (optional, matches your other frames)
        tk.Frame(admin_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=5)

        # Total Sales section
        sales_frame = tk.Frame(admin_frame)
        sales_frame.pack(pady=10, padx=5, anchor=tk.W)

        # Label
        tk.Label(sales_frame, text="Total Sales:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
        self.total_sales_var = tk.StringVar()
        self.total_sales_var.set("$0")  # Set initial value

        # Read-only text field
        self.total_sales_field = tk.Entry(
            sales_frame,
            width=15,
            state='readonly',  # Makes it read-only
            readonlybackground='white',  # Background color when readonly
            font=('Helvetica', 10),
            relief=tk.FLAT,  # Makes it look flat (optional)
            textvariable = self.total_sales_var
        )
        self.total_sales_field.pack(side=tk.LEFT, padx=5)

        # You can set initial value like this:
        self.total_sales_field.config(state='normal')
        self.total_sales_field.config(state='readonly')


        # Total Customers section (new frame)
        customers_frame = tk.Frame(admin_frame)
        customers_frame.pack(pady=5, padx=5, anchor=tk.W)  # pady=5 for spacing

        self.total_customers_var = tk.StringVar()
        self.total_customers_var.set("{}".format(event.get_total_customers()))  # Set initial value

        # Customers Label + Field
        tk.Label(customers_frame, text="Total Customers:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
        self.total_customers_field = tk.Entry(
            customers_frame,
            width=15,
            state='readonly',
            readonlybackground='white',
            font=('Helvetica', 10),
            relief=tk.FLAT,
            textvariable=self.total_customers_var
        )
        self.total_customers_field.pack(side=tk.LEFT, padx=5)

        # to update
        # self.total_customers_var.set(new_value)


        # Total Customers section (new frame)
        policy_frame = tk.Frame(admin_frame)
        policy_frame.pack(pady=5, padx=5, anchor=tk.W)  # pady=5 for spacing

        self.policy_var = tk.StringVar()
        self.policy_var.set(policy.get_policy_details())

        # Customers Label + Field
        tk.Label(policy_frame, text="Discount Policy:", font=('Helvetica', 10, 'bold')).pack(side=tk.LEFT)
        self.policy_field = tk.Entry(
            policy_frame,
            width=15,
            state='readonly',
            readonlybackground='white',
            font=('Helvetica', 10),
            relief=tk.FLAT,
            textvariable=self.policy_var
        )
        self.policy_field.pack(side=tk.LEFT, padx=5)

        # Discount On button
        tk.Button(
            admin_frame,
            text="Discount On",
            font=('Helvetica', 9),
            bg='#4CAF50',
            command=self.enable_discount_policy
        ).pack(pady=(0, 2), padx=5, anchor=tk.W)  # Small bottom padding

        # Discount Off button
        tk.Button(
            admin_frame,
            text="Discount Off",
            font=('Helvetica', 9),
            bg='#f44336',
            command=self.disable_discount_policy
        ).pack(pady=(0, 5), padx=5, anchor=tk.W)  # Larger bottom padding

        # Separator line (optional, matches your other frames)
        tk.Frame(admin_frame, height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, pady=5)




        ## Right panel for existing content
        right_frame = tk.Frame(content_frame)
        right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)


    def account_management_output(self, new_text):
        """
        This method takes in a message string and clears the previous output for
        account management output window and displays the message.
        """
        # Clear the current content
        self.output_text.config(state='normal') 
        self.output_text.delete('1.0', tk.END) 

        # Insert the new text
        self.output_text.insert(tk.END, new_text)
        self.output_text.config(state='disabled')  

        # Auto-scroll to the bottom to show latest content
        self.output_text.see(tk.END)

    def booking_output(self, new_text):
        """
        This method takes in a message string and clears the previous output for
        booking output window and displays the message.
        """
        # Clear the current content
        self.booking_output_text.config(state='normal')  
        self.booking_output_text.delete('1.0', tk.END)  

        # Insert the new text
        self.booking_output_text.insert(tk.END, new_text)
        self.booking_output_text.config(state='disabled')  
        
        # Auto-scroll to the bottom to show latest content
        self.booking_output_text.see(tk.END)

    def open_add_customer_window(self):
        '''
        Method for a new window display for adding a new customer.
        :return: 
        '''
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Customer")
        add_window.geometry("300x200")

        # Form fields
        tk.Label(add_window, text="ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_window, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(add_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)

        self.id_entry = tk.Entry(add_window)
        self.name_entry = tk.Entry(add_window)
        self.email_entry = tk.Entry(add_window)
        self.phone_entry = tk.Entry(add_window)

        self.id_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.email_entry.grid(row=2, column=1, padx=5, pady=5)
        self.phone_entry.grid(row=3, column=1, padx=5, pady=5)

        submit_btn = tk.Button(add_window, text="Submit", command=self.submit_customer)
        submit_btn.grid(row=4, columnspan=2, pady=10)

    def submit_customer(self):
        '''
        This method is called when the user submits for adding a new customer.
        It creates a customer object and registers that customer into the system as well.
        :return: 
        '''
        id =  self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        customer_data = {
            "id": id,
            "name": name,
            "email": email,
            "phone": phone
        }

        if id != "" and name != "" and email != "" and phone != "":

            print("New Customer Details:")
            print(f"ID: {customer_data['id']}")
            print(f"Name: {customer_data['name']}")
            print(f"Email: {customer_data['email']}")
            print(f"Phone: {customer_data['phone']}")

            customer = Customer(id,name,email,phone)
            event.register_customer(customer)
            customer.save_to_file()

            current_customers = int(self.total_customers_field.get())
            current_customers += 1
            self.total_customers_var.set(current_customers)

            self.id_entry.master.destroy()

        else:
            print("Missing Information!")

    def delete_customer(self):
        '''
        THis method reads the id from the field and removes the customer from the event system.
        :return: 
        '''
        id = self.del_entry.get()
        customer = event.get_customer_by_id(id)
        if customer:
            event.unregister_customer(customer)
            msg = "Customer with ID {} deleted.".format(id)
            self.account_management_output(msg)

        else:
            msg = "Customer with the id {} not found".format(id)
            self.account_management_output(msg)

    def customer_details(self):
        '''
        This method finds the details of the customer for the given ID and displays
        those details in the output.
        :return: 
        '''
        id = self.details_entry.get()
        customer = event.get_customer_by_id(id)
        if customer:
            details = customer.__str__()
            self.account_management_output(details)
        else:
            msg = "Customer with the id {} not found".format(id)
            self.account_management_output(msg)

    def enable_discount_policy(self):
        policy.enable_discount()
        self.policy_var.set(policy.get_policy_details())

    def disable_discount_policy(self):
        policy.disable_discount()
        self.policy_var.set(policy.get_policy_details())

    def update_dashboard(self):
        '''
        This method refreshes the sales amount on the dashboard
        :return: 
        '''
        msg = "${}".format(event.get_total_sales())
        self.total_sales_var.set(msg)


    def book_ticket(self):
        '''
        This method reads the customer id, payment method, ticket type and creates the ticket
        and then adds that ticket into the event for keeping track of the sales also 
        provides it to the customer.
        '''
        global seat_number

        customer_id = self.customer_id_entry.get()
        customer = event.get_customer_by_id(customer_id)
        # print(customer_id)
        if customer:
            payment_method = self.payment_method.get()
            ticket_type = self.ticket_type.get()
            seat_number += 1
            print(ticket_type)
            if ticket_type == "Single-Race Passes":
                ticket = SingleRaceTicket(single_race_ticket_price,seat_number)
                event.add_ticket_sale(ticket)
                customer.add_purchase(ticket)
                msg = "Ticket : {} sold to\nCustomer : {}".format(ticket_type,customer.get_name())
                self.booking_output(msg)

            elif ticket_type == "Season Ticket":
                ticket = SeasonMembershipTicket(season_membership_ticket_price,seat_number)
                event.add_ticket_sale(ticket)
                customer.add_purchase(ticket)
                msg = "Ticket : {} sold to\nCustomer : {}".format(ticket_type,customer.get_name())
                self.booking_output(msg)

            elif ticket_type == "Weekend Packages":
                ticket = WeekendPackageTicket(season_membership_ticket_price,seat_number)
                event.add_ticket_sale(ticket)
                customer.add_purchase(ticket)
                msg = "Ticket : {} sold to\nCustomer : {}".format(ticket_type,customer.get_name())
                self.booking_output(msg)

            self.update_dashboard()
        else:
            msg = "Customer not found"
            self.booking_output(msg)



if __name__ == "__main__":
    import tkinter as tk
    import tkinter.font as tkfont
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()












