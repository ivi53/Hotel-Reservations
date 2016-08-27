# Hotel Reservations
A console application with the functionality of a reservation system.

When the application starts, you are faced with three main options.
You can either just browse the different prices and discounts without being a client. But that way you won't be able to take a
reservation or do anyrhing else. 
The secoond option is to register into the system if you still don't have a profile. A confirmation email is send after that.
And the third main option is to login with your exsisting account.

If the login is successful you are either treated as a client or as an admnistrator depending on the username given during login.
The ones considered clients are faced with many options after the successful login.
They can once again view the different prices and discounts but they can also make a reservation. See the reservations that are in the
future. Later they can decide to cancel a reservation or to pay an upcoming one. They can also check how many visits do the have so far and what is the discount. Finally, clients can change their password or bank account.
The ones considered administrators are separated into 3 more roles. The first is a database admin, who can add or delete stuff from some of the tables in the database. The second is a receptionist, they can make, cancel or check a reservation and also add problems to a certain reservation. The third role is the manager. He/She can hire or fire receptionists. He/She can also update prices and discounts. Also reservations can be made or cancelled from here as well. And rooms can be added or removed from the database.

Reservations are made with the input of begin and end dates, number of adults, number of children, the type of feeding. After the
available rooms are found a type can be chosen. The different types have different extras whih are priced separately.
Users are able to decline a reservation but if it is one week before the arrival 50% of their whole stay will be taken from their
accounts.

Emails will also be send when a reservation is made, cancelled or payed.
