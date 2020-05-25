
**SIGN UP USER**
----
Returns json data about acknowledgement.

* **URL**

  /signup
  
* **Headers:**

    `Content-Type - Application/Json`


* **Method:**

  `POST`
  
*  **URL Params**

   **Required:**
 
   `id=[integer]`

* **Data Params**

  **Required:**
 
   `name - String`
   `email - String`
   `password - String`

---


**Login USER**
----
Returns json data having token.

* **URL**

  /login
  
* **Headers:**
    
    `Content-Type - Application/Json`

* **Method:**

  `POST`

* **Data Params**

  **Required:**
 
   `email - String`
   `password - String`

---

**CREATING MOVIE**
----
Movie object returned with id.

* **URL**

  /movies

* **Method:**

  `POST`

* **Headers:**
    `Content-Type - Application/Json`
    `token - String`

* **Data Params**

  **Required:**
 
   `title - String`
   `email - String`
   `password - String`

---

**Editing MOVIE**
----
Only user who have created movie can edit the movie

* **URL**

  /movies/:id

* **Method:**

  `PUT`

* **Headers:**
    `Content-Type - Application/Json`
    `token - String`

* **Data Params**

  **Required:**
 
   `title - String`

---

**DELETE Movie**
----
Movie object returned with id.

* **URL**

  /movies/:id

* **Method:**

  `DELETE`

* **Headers:**

    `Content-Type - Application/Json`
    
    `token - String`

* **Data Params**

  **Not Required**

---


**Getting MOVIE**
----
Movie object returned with id. If id is not specified all movies are returned

* **URL**

  /movies/:id

* **Method:**

  `GET`

* **Headers:**

    `Content-Type - Application/Json`

* **Data Params**

  **Not Required**

---

**RATINGS**
---

**CREATING Rating**
----
Rating object returned with id. Pass rating value with `value` parameter.
Creator of the movie cannot rate a movie.

* **URL**

  /ratings

* **Method:**

  `POST`

* **Headers:**

    `Content-Type - Application/Json`
    
    `token - String`

* **Data Params**

  **Required:**
 
   `movie_id - Integer`
   `value - Integer`

---

**Editing Rating**
----
Only user who have created rating can edit it.

* **URL**

  /ratings/:id

* **Method:**

  `PUT`

* **Headers:**
    `Content-Type - Application/Json`
    `token - String`

* **Data Params**

  **Required:**
 
   `value - Integer`

---

**DELETE Rating**
----
Only user who created rating can delete it.

* **URL**

  /ratings/:id

* **Method:**

  `DELETE`

* **Headers:**

    `Content-Type - Application/Json`
    
    `token - String`

* **Data Params**

  **Not Required**

---


**Getting Ratings**
----
Movie object returned with id. If id is not specified all ratings are returned.

* **URL**

  /ratings/:id

* **Method:**

  `GET`

* **Headers:**

    `Content-Type - Application/Json`

* **Data Params**

  **Not Required**

---

