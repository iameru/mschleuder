# development data

this is just a quick write up with some data for different webpages as I want to try out designing some portions before taking care of the backend

## stations

Stations is a overview page of stations to deliver to. It includes some historical data of stations, a method to add a new and change existing ones.


[testmark]:# (stations-current)
```json
[
 { "id":1, "order":2, "info":"Kackstraße 15, marianne", "name":"Ost", "members_full":32, "members_half":15 },
 { "id":3, "order":1, "info":"Weit draussn beim platz", "name":"West", "members_full":12, "members_half":5 },
 { "id":4, "order":5, "info":"Steven, kontakt 027 // 1238 27 199", "name":"Süd", "members_full":26, "members_half":19 },
 { "id":5, "order":3, "info":"erna anklingeln vorher", "name":"Ost II", "members_full":2, "members_half":2 },
 { "id":6, "order":4, "info":"mariannenplatz 123, anrufen: 0182 / 23723 211 1", "name":"West II", "members_full":20, "members_half":8 },
 { "id":8, "order":6, "info":"bratwursthund 123, 04315 Leipzig", "name":"Nord", "members_full":10, "members_half":6 }
]
```

historische daten zbsp:
[testmark]:# (stations-historical)
```json
[
 { "date":"2022-08-08", "stations":
   [
    { "id":1, "members_full":32, "members_half":15 },
    { "id":3, "members_full":12, "members_half":5 },
    { "id":4, "members_full":26, "members_half":19 },
    { "id":5, "members_full":2, "members_half":2 },
    { "id":6, "members_full":20, "members_half":8 },
    { "id":8, "members_full":10, "members_half":6 }
   ]
 },
 { "date":"2022-08-05", "stations":
   [
    { "id":1, "members_full":33, "members_half":14 },
    { "id":3, "members_full":12, "members_half":5 },
    { "id":4, "members_full":23, "members_half":19 },
    { "id":5, "members_full":1, "members_half":4 },
    { "id":6, "members_full":20, "members_half":6 },
    { "id":8, "members_full":10, "members_half":6 }
   ]
 },
 { "date":"2022-08-03", "stations":
   [
    { "id":1, "members_full":35, "members_half":15 },
    { "id":3, "members_full":11, "members_half":6 },
    { "id":4, "members_full":22, "members_half":12 },
    { "id":5, "members_full":2, "members_half":5 },
    { "id":6, "members_full":21, "members_half":5 },
    { "id":8, "members_full":10, "members_half":5 }
   ]
 }
]
```


## products

Products is a overview page of products/vegetables to distribute. It includes some historical data, a method to add new and change existing ones.


[testmark]:# (products)
```json
[
 { "id":1, "name":"kartoffeln", "unit":"kg", "info":"" },
 { "id":3, "name":"möhren", "unit":"kg", "info":"" },
 { "id":4, "name":"zwiebeln", "unit":"kg", "info":"schmecken super" },
 { "id":5, "name":"kohlrabi", "unit":"pc", "info":"" },
 { "id":6, "name":"melonen", "unit":"pc", "info":"die gelben" },
 { "id":8, "name":"petersilie", "unit":"bnd", "info":"" }
]
```

mit historische daten zbsp:
[testmark]:# (products-historical)
```json
[
 { "id":1, "name":"kartoffeln", "unit":"kg", "info":"", "distributed":
   {
     "2022-08-03":55,
     "2022-08-05":94,
     "2022-08-08":45
   }
 },
 { "id":5, "name":"kohlrabi", "unit":"pc", "info":"", "distributed":
   {
     "2022-08-05":90
   }
 },
 { "id":8, "name":"petersilie", "unit":"bnd", "info":"" }
]
```


## history

History will be an overview with detailed insights on different distributions made in the past. all information will be accessable in one way or another. this might be many data
