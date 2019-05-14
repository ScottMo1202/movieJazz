# movieJazz

You must provide documentation of your endpoints and database in the README.md file. You should use markdown and code blocks where appropriate to make it easier to find things in the document.

For each endpoint, include: endpoint route, what behavior it has (implemented HTTP method, status codes, error messages it can return, what it changes in the database, who use the route).

For any non-GET HTTP method, you should include an example input and output. For example, the user might post a JSON object with 3 fields and get some JSON response back.

### Endpoints
* /main/theaters: refers to all theaters<br />
   * GET: Respond with a list of all of the theaters in the database with a status of 200. It will return Database error message if bugs happen. Anyone can do this even without any authentification.
   * POST: Create a new theater, save it into the database using the theater model JSON in the request body, respond with a 201 code and a copy of the new theater model encoded as a json object. Only the administrator and the seller can do it. It may return Database error or KeyError messages.

* /main/theaters/{theater_id}: refers to a specific theater
   * GET: Respond with information of the specific theater as a json object with a status of 200. It will return Database error if bugs happen. Anyone cna do this even without any authentification.
   * PATCH: modify information of the specific theater using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated theater encoded as a json objet. Only the administrator and the seller can do it. It will return Database Error or KeyError messages when bugs happen.
   * DELETE: delete the specified channel in the database according to the parameter in the url and respond with a HttpResponse with 'deleted' if succeed. It may also return Database error message if there are errors in the code. Only the administrator and seller are authorized to do this.
* /main/tickets: refers to all movie tickets in the Database
   * GET: Respond with a list of all of the tickets in the database that belong to the current user with a status code of 200. If something goes wrong, it will reply Database Error. Every user can do this after authentification
   * POST: Create a new ticket, save it into the database using the ticket model JSON in the request body, respond with a 201 code and a copy of the new ticket encoded as a json object. Only the administrator and the seller can do it. It may return Database error message or KeyError message if something goes wrong.
   * DELETE: delete the specified ticket in the database according to the JSON object in the request body. Respond with a HttpResponse with 'deleted' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
* /main/transactions: refers to all transactions in the Database
   * GET: Respond with a list of all of the tickets in the database witha  status code of 200. If something goes wrong, it reply with a Database Error Message. Only the administrator can use this route.
   * POST: Create a new transaction model, save it into the database using the transaction model JSON in the request body, respond with a 201 code and a copy of the new transaction encoded as a json objet. Only the administrator can do this action. It will return Database error message or KeyError message if something goes wrong.
   * DELETE: delete the specified transaction in the database according to the JSON object in the request body. Respond witha  Http Response with 'delete' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
* /movies: refers to all movies in the Database
   * GET: Respond with a list of all of the movies in the database with a status of 200. It will return Database error message if bugs happen. Anyone can do this even without any authentification.
   * POST: Create a new movie, save it into the database using the movie model JSON in the request body, respond with a 201 code and a copy of the new movie encoded as a json object. Only the administrator can do it. It may return Database error message if something goes wrong.
* /movies/{movie_id}: refers to a specific movie
   * GET: Respond with information of the specific movie as a json object with a status of 200. It will return Database error if bugs happen. Anyone can do this even without any authentification.
   * PATCH: modify information of the specific movie using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated movie encoded as a json objet. Only the administrator can do it. It will return Database Error or KeyError messages when bugs happen.
   * DELETE: delete the specified movie in the database according to the JSON object in the request body. Respond with a  Http Response with 'This movie was deleted' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.

* /users: refers to all users in the Database
   * GET: Respond with a list of all of the users in the database with a status of 200. It will return Database error message if bugs happen. Only the administrator can do this.

* /offers: refers to all offers in the database
   * GET: Respond with a list of all of the offers in the database with a status of 200. It will return Database error message if bugs happen. Anyone can do this even without any authentification.
   * POST: Create a new offer, save it into the database using the offer model JSON in the request body, respond with a 201 code and a copy of the new offer encoded as a json object. Only the administrator can do it. It may return Database error message if something goes wrong.

* /offers/{offer_id}: refers to a specific offer
   * GET: Respond with information of the specific offer as a json object with a status of 200. It will return Database error if bugs happen. Anyone can do this even without any authentification.
   * PATCH: modify information of the specific offer using the JSON object in the request body, save new changed into the database, respond with a 201 and a copy of the newly updated offer encoded as a json objet. Only the administrator can do it. It will return Database Error or KeyError messages when bugs happen.
   * DELETE: delete the specified offer in the database according to the JSON object in the request body. Respond with a  Http Response with 'This offer was deleted' if succeed. It will return Database error message if there are errors in the code. Only the administrator can handle this action.
