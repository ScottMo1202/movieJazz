# movieJazz
![](./database-schema.png)

We created an admin account automatically as the server starts, some requests are restricted only to admins. This will be mentioned in the later as well.  <br />
admin username: admin<br />
admin password: admin<br />

For every newly registered user, the default membership is normal.<br />
### Endpoints
* /main/theaters: refers to all theaters<br />
   * GET: list all theaters information to the template, including name, address, city, state, postal code, and a button to see all tickets each sells. Anyone can do this even without any authentification. Code sent: 200. <br />
   Example: <br />
   ![alt text](./img/theaters.png)
   * POST: Create a new theater, save it into the database using the theater model JSON in the request body, respond with a 201 code and a copy of the new theater model encoded as a json object. Only the administrator and the seller can do it. It may return Database error or KeyError messages.
   * Sample input:<br />
   {<br />
     "name": "regal",<br />
     "street_number": 123, <br />
     "street_name": "University way", <br />
     "city": "Seattle", <br />
     "state": "WA",<br />
     "post_code": "98105"<br />
   }<br />
   * Sample output:<br />
   {<br />
     "id": 2, <br />
     "name": "regal",<br />
     "street_number": 123, <br />
     "street_name": "University way", <br />
     "city": "Seattle", <br />
     "state": "WA",<br />
     "post_code": "98105"<br />
   }

* /main/theaters/{theater_id}: refers to a specific theater
   * GET: Respond with information of the specific theater as a json object with a status of 200. It will return Database error if bugs happen. Anyone can do this even without any authentification.
     * Sample input:<br />
    {<br />
      "name": "Regal Theaters",<br />
      "street_number": "1234", <br />
      "street_name": "Brooklyn Avenue", <br />
      "city": "Seattle", <br />
      "state": "WA", <br />
      "post_code": "98105" <br />
    }<br />

   * PATCH: modify information of the specific theater using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated theater encoded as a json objet. Only the administrator and the seller can do it. It will return Database Error or KeyError messages when bugs happen.
     * Sample input:<br />
    {<br />
      "name": "amc",<br />
      "street_number": 133, <br />
      "street_name": "University of Washington way", <br />
      "city": "Seattl", <br />
    }<br />
    * Sample output:<br />
   {<br />
     "id": 1 <br />
     "name": "amc",<br />
     "street_number": 133, <br />
     "street_name": "University of Washington way", <br />
     "city": "Seattl", <br />
   }<br />
   * DELETE: delete the specified channel in the database according to the parameter in the url and respond with a HttpResponse with 'deleted' if succeed. It may also return Database error message if there are errors in the code. Only the administrator and seller are authorized to do this.
  * Sample output:<br />
  "Deleted"<br />

* /main/theaters/{theater_id}/movies: refers to all movie played in the theater
  * GET: Respond with a list of all of the movies in the database that are played in the theater. code sent: 200. Any one can do this without any authentification. <br />
  Example: <br />
  ![alt text](./img/theaterMovies.png)

* theaters/{int:theater_id}/movies/{movie_id}/tickets: refers to all tickets of a movie in a specified theater
  * GET: List the ticket information, including show time, movie type, price, seats left. code sent: 200. Anyone can do this without any authentification<br />
  Example: <br />
  ![alt text](./img/tickets.png)
  * POST: post new tickets to the database according to the two parameters in the url and returns a json object if succeed. Only the administrator can do this. Code sent: 201
  * Sample input:<br />
   {<br />
     "time": "2019-04-18T18:53:12Z",<br />
     "price": 9.16, <br />
     "movie_type": "RE", <br />
     "amount": 60, <br />
   }<br />
  * Sample output: <br />
    {
    "id": 7, <br />
    "movie_id": 2, <br />
    "time": "2019-04-18T18:53:12Z", <br />
    "theater_id": 3, <br />
    "price": "9.16", <br />
    "amount": 60, <br />
    "movie_type": "RE" <br />
    }
  * DElETE: delete tickets of a specific movie in a specified theater and return with a plain http response"Ticket Deleted" if succeed. code sent: 201. Only the administrator can do this

* /main/transactions: refers to all tickets transactions of the currentuser in the Database
   * GET: Renders a list of all tickets transactions that the current user made before. Code sent, the user has to login to complete this operation.
   Example: <br />
   ![alt text](./img/ticketTransaction.png)
   * POST: Create a new transaction model, save it into the database using the transaction model JSON in the request body, respond with a 201 code and a copy of the new transaction encoded as a json objet. Only the administrator can do this action. It will return Database error message or KeyError message if something goes wrong.
   * Sample input:<br />
   {<br />
     "user": 1,<br />
     "ticket": 1, <br />
     "quantity": 3, <br />
     "offer": 1, <br />
   }
   * Sample output:<br />
   {<br />
     "id": 2, <br />
     "user": 1,<br />
     "ticket": 1, <br />
     "quantity": 3, <br />
     "offer": 1, <br />
     "total_price": 12.88, <br />
     "date": "2019-04-18T18:53:12Z"<br />
   }
   * DELETE: delete the specified ticket transaction in the database according to the JSON object in the request body. Respond witha  Http Response with 'delete' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
   * Sample input:<br />
     {<br />
       "id": 1<br />
     }
   * Sample output:<br />
   "transaction Deleted"
* /movies: refers to all movies in the Database
   * GET: List all movies and their related information, including name, short description, and runtime. Anyone can do this even without any authentification. Code snet: 200 <br />
   Example: <br />
   ![alt text](./img/movies.png)
   * POST: Create a new movie, save it into the database using the movie model JSON in the request body, respond with a 201 code and a copy of the new movie encoded as a json object. Only the administrator can do it. It may return Database error message if something goes wrong.
   * Sample input:<br />
   {<br />
     "name": "Avengers:endgame", <br />
     "description": "This is Avengers", <br />
     "runtime": 120, <br />
   }
   * Sample output:<br />
   {<br />
     "id": 3
     "name": "Avengers:endgame", <br />
     "description": "This is Avengers", <br />
     "runtime": 120, <br />
   }
* /movies/{movie_id}: refers to a specific movie
   * GET:  Display information for a specified movie, including its name, runtime, and a review button if the user wants to rate it. Anyone can do this even without any authentification. code sent: 200<br />
   Example: <br />
   ![alt text](./img/specificMovie.png)
   * PATCH: modify information of the specific movie using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated movie encoded as a json objet. Only the administrator can do it. It will return Database Error or KeyError messages when bugs happen.
   * Sample input:<br />:
   {<br />
     "name": "Lion King", <br />
     "description": "This is lions", <br />
   }<br />

   * Sample output:<br />:
   {<br />
     "id": 2,
     "name": "Lion King", <br />
     "description": "This is lions", <br />
   }<br />

   * DELETE: delete the specified movie in the database according to the parameter in the url. Respond with a  Http Response with 'This movie was deleted' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
   * Sample output:<br />:
   "Movie deleted"<br />

* movies/raw: refer all movies data in a json Response
  * GET: Retrieve all movie data form the database and return it as a json object. Code sent: 200, anyone can do this without authentification.
  Example: <br />
  ![alt text](./img/rawMovies.png)

* movies/search: a user can search a movie in the database
  * GET: renders a search bar where user can type the movie he wants. code sent: 200. Anyone can do this without authentification.
  Example: <br />
  ![alt text](./img/searchMovie.png)
  * POST: based on the query the user submits, finds all movies names that contains all leters of the user input and renders all movies. code sent: 200. Anyone can do this without any authentification.
  Example: <br />
  ![alt text](./img/searchResult.png)

* movies/{movie_id}/review: allows the user to rate the movie specified in the url.
  * GET: renders a review form, where the user can rate the movie from terrible to excellent, and write his comments.
  Example: <br />
  ![alt text](./img/reviewForm.png)
  * POST: Create a new review model and save it in the database based on what the user fill in the review-form. It will return a plain HttpResponse"Thanks for rating" if succeeds. code sent: 201. The user has to login to do this operation.

* /users: refers to all users in the Database
   * GET: Respond with a list of all of the users in the database with a status of 200. It will return Database error message if bugs happen. Only the administrator can do this.
   Example: <br />
   ![alt text](./img/users.png)

* /offers: refers to all offers in the database
   * GET: Respond with a list of all of the offers in the database with a status of 200. It will return Database error message if bugs happen. Anyone can do this even without any authentification.
   * POST: Create a new offer, save it into the database using the offer model JSON in the request body, respond with a 201 code and a copy of the new offer encoded as a json object. Only the administrator can do it. It may return Database error message if something goes wrong.
   * Sample input:<br />
   {<br />
     "offer_name": "30% off", <br />
     "offer_perc": 0.70, <br />
     "description": "this is an offer"<br />
   }<br />
   * Sample output:<br />
   {<br />
     "id": 2, <br />
     "offer_name": "30% off", <br />
     "offer_perc": 0.70, <br />
     "description": "this is an offer"<br />
   }<br />

* /offers/{offer_id}: refers to a specific offer
   * GET: Respond with information of the specific offer as a json object with a status of 200. It will return Database error if bugs happen. Anyone can do this even without any authentification.
   * PATCH: modify information of the specific offer using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated offer encoded as a json objet. Only the administrator can do it. It will return Database Error or KeyError messages when bugs happen.
   * Sample input:<br />:
   {<br />
     "offer_name": "30% off", <br />
     "description": "this is an offer"<br />
   }<br />
   * Sample output:<br />:
   {<br />
     "id": 3, <br />
     "offer_name": "30% off", <br />
     "description": "this is an offer"<br />
   }<br />
   * DELETE: delete the specified offer in the database according to parameter in the url. Respond with a  Http Response with 'This offer was deleted' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
   * Sample output:<br />:
   "Offer deleted"<br />

* contact/
  * GET: renders a form, where the user can fill their first name, last name, email, the question and choose which type of question they want to ask. Anyone can do this even without any authentification. code sent: 200. <br />
  Example: <br />
  ![alt text](./img/contact.png)
  * POST: Post the question the users asked into the data. If succeeds, the system will respond with a HttpResponse 'Thank you for posting questions.' code sent: 201. <br />
  Example: <br />
  ![alt text](./img/questionPost.png)

* contact/questions/
  * GET: List all questions users posted and their answers. Some have been provided answers, and some have not. code sent: 200. Anyone can do this even without any authentification, but only the administrator can see the 'procide answer' button<br />
  Example: <br />
  ![alt text](./img/questions.png)

* contact/answer/{question_id}/
  * GET: renders a form, where the administrator can answer the question specified in the url. code sent: 200. Only the administrator can do this. code sent: 200<br />
  * Post: The new answer will be stored in the database. If succeeds, the system will reply with HttpResponse: 'Thank you for answering'. code sent: 201. Only the administrator can do this. <br />

* auth/signin/
  * GET: renders a signin form, where the user needs to fill his username and password. code sent; 200. Anyone can do this without any authentification. <br />
  Example: <br />
  ![alt text](./img/signin.png)
  * POST: If the filled username exists in the database and the password matches. the server will allow the user to login and redirect to the homepage.

* auth/register
 * GET: renders a registration form, where the user needs to fill his username, password, password comfirmation, fist name, last name, and email to sign up a new account. code sent: 200. Anyone can do this without any authentification. <br />
 Example: <br />
 ![alt text](./img/register.png)
 * POST: Post the new user data to the database if the user fills all data appropriately and redirect to the signin form. code sent: 201. Anyone can do this without any authentification. <br />

 * user/
   * GET: list all data profile that the user current has. code sent: 200. The user has to login to do this operation.<br />
   Example: <br />
   ![alt text](./img/userProfile.png)

* user/memberships: list all membership options
  * GET: list all membership options that the user can buy. code sent: 200. The user has to login to this operation.
  Example: <br />
  ![alt text](./img/memberships.png)

* 'user/memberships/purchase/<int:theType>': allows user to buy a specified membership based on the url
  * GET: renders a list where user can fill all of his information to update the membership. <br />
  Example: <br />
  ![alt text](./img/specificMembership.png)
  * POST: create a new membership transaction model and save it into the database. Reply with a plain HttpResponse if succeed("Thanks for purchasing")code sent: 201. The user has to login to do this.<br />

* user/transactions: refers to all membership transaction of the current user
  * GET: renders a list of all membership transaction. code sent:200. The suer has to login to do this.
  Example: <br />
  ![alt text](./img/memberTrans.png)



* cart/
  * GET: display all items(tickets) that the user intends to buy, for each item, it displays its id, quantity, movie name, offer name, total_price. code sent: 200. The user has to login to do this operation.
  Example: <br />
  ![alt text](./img/cart.png)

* cart/<int: cart_id>
  * GET:

* cart/checkout
  * GET: renders a checkout form when the user plans to pay for all items in his cart. The users neess to fill name_on_card, billing_address, card_number and csv code to finish this purchase. code sent: 200.  The user has to be authenticated to do this operation.
  * POST:
