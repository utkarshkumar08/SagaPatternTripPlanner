# SagaPatternTripPlanner
Saga Pattern based Trip Planner which includes Flight booking, Hotel Booking, Car Booking
Problem Statement: 
Distributed systems do not implement ACID in complex long running transactions. You have propose an architecture of toy BITSTripOrganizer application which will do i) Hotel booking ii) Car booking iii) Flight booking. For a given user, when all the three are successful, the trip is created with a unique TripID. The user should register with some details (you decide). The flight booking process will show a set of flights for a given ”from and to” locations using an external service (imagine that such a service exists). The payment will be done through an external payment gateway. After the payment, the flight booking should be done by sending a booking request to this external service. The hotel booking process will show a list of hotels based on the booked flight. This list will be available from an external service (imagine that such a service exists). The hotel booking will be done through the same payment gateway and a similar process will be followed to book the hotel room. Once the hotel booking is done, then it will give a list of car booking options, obtained from an external service. Once the car booking is complete, then we consider the trip creation to be complete. A successful trip creation will result in an unique trip-id and the necessary details will be stored in the application’s own OLTP database. The transaction will fail if any of the intermediate task fails. In that case, the system should generate an appropriate compensatory transaction. For instance, if a flight booking is complete but hotel booking fails, then flight booking should also be cancelled by sending a ”cancel-booking” request to the same external service that provided the list of flights.
Such a system is popularly implemented using Saga pattern (proposed in 1987 from Cornell). Read https: //microservices.io/patterns/data/saga.html for more details. Saga pattern is implemented in Java based Eventuate framework. Go through https://github.com/eventuate-examples/eventuate-examples-java-aws- gateway-echo and https://eventuate.io for details.

Model : Define the logical, physical and process views using StarUML. Show the use-cases. You can use package to model a component or a service. Use stereotypes to indicate which one is external and which one is internal module.

Dynamics : Define a few sequence diagrams for important scenarios.

Working prototype.

Implementation :
Saga is a sequence of local transactions where each local transaction performs the task
assigned to it and triggers the next transaction. There are two types of architectures in Saga pattern namely Choreography based pattern and Orchestration based pattern. We chose Orchestration based pattern due to following reasons:
  1. It maintains data consistency across multiple services without distributed transactions
  2. It helps avoid cyclic dependency when multiple external services are used
  3. Highly decoupled architecture
The only drawback is the possibility of Orchestrating Saga becoming complex and directing dumb logic in other Sagas.


There are 6 Sagas in the design which are as follows:
  1. User registration
  2. Control
  3. Flight Booking
  4. Hotel Booking
  5. Car Booking
  6. End
User Registration Saga : It provides facility for the User to register and Login before starting any kind of bookings.

Control Saga: It is the critical logic in this Orchestration based architecture. It commands the other Sagas and maintains Idempotency, Consistency and also triggers the compensating transactions in case of any failure. 
Event Sourcing is used to maintain the state and provide a log of the changes made in the states.
There is an internal database which stores multiple locks and booking status attributes to maintain the state of the booking and assure Idempotency. The updates to this internal database and commands to the Sagas are atomic to maintain consistency.

Flight Booking Saga, Hotel Booking Saga and Car booking: They work according to the directions of the Control Saga and books the corresponding entities by communicating with the External Booking Service and Payment Gateway and send the Booking status to the Control Saga. They also execute the cancellation compensating transactions whenever the Control Saga directs.

End Saga: It updates the OLTP database after successful completion of the Trip Booking. It is the final Saga and cannot fail.
If any changes are made to Flight booking Saga, Hotel Booking Saga or Car Booking Saga, it will be communicated only to Control Saga which makes this architecture highly decoupled and eliminates cyclic dependencies amongst the various Booking Sagas.
