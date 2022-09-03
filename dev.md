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
    { "id":6, "members_full":20, "members_half":8 },
    { "id":8, "members_full":10, "members_half":6 }
   ]
 },
 { "date":"2022-08-05", "stations":
   [
    { "id":1, "members_full":33, "members_half":14 },
    { "id":2, "members_full":20, "members_half":3 },
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
    { "id":2, "members_full":8, "members_half":1 },
    { "id":3, "members_full":11, "members_half":6 },
    { "id":4, "members_full":22, "members_half":12 },
    { "id":5, "members_full":2, "members_half":5 },
    { "id":6, "members_full":21, "members_half":5 },
    { "id":8, "members_full":10, "members_half":5 }
   ]
 },
 { "date":"2022-07-23", "stations":
   [
    { "id":1, "members_full":36, "members_half":15 },
    { "id":3, "members_full":10, "members_half":4 },
    { "id":4, "members_full":20, "members_half":2 },
    { "id":5, "members_full":1, "members_half":4 },
    { "id":6, "members_full":20, "members_half":2 },
    { "id":8, "members_full":5, "members_half":3 }
   ]
 }
]
```


Es soll einen chart geben der die stationen und ihren mitgliederverlauf darstellt


[testmark]:# (stations-chart)
```json
[
 { "date":"2022-08-05", "stations":
   [
    { "id":1, "members_full":4, "members_half":4 },
    { "id":5, "members_full":8, "members_half":8 }
   ]
 },
 { "date":"2022-08-03", "stations":
   [
    { "id":1, "members_full":2, "members_half":2 },
    { "id":5, "members_full":4, "members_half":4 }
   ]
 },
 { "date":"2022-07-23", "stations":
   [
    { "id":1, "members_full":1, "members_half":1 },
    { "id":5, "members_full":2, "members_half":2 }
   ]
 }
]

```


## products

Products is a overview page of products/vegetables to distribute. It includes some historical data, a method to add new and change existing ones.
it should show some recently used products on top, underneath a somewhat searchable productlist, either with search or with startingletter hints.


[testmark]:# (products)
```json
 [
 { "recent_distribution": "2022-08-28", "id":20, "unit":"g", "order":3, "name":"Rucola", "info":"" },
 { "recent_distribution": "2022-08-27", "id":21, "unit":"kopf", "order":1, "name":"Feldsalat ", "info":"" },
 { "recent_distribution": "2022-08-26", "id":22, "unit":"st.", "order":2, "name":"Porree", "info":"" },
 { "recent_distribution": "2022-08-28", "id":23, "unit":"g", "order":19, "name":"Asiasalat", "info":"" },
 { "recent_distribution": "2022-08-28", "id":24, "unit":"kg", "order":20, "name":"Spinat", "info":"" },
 { "recent_distribution": "2022-08-25", "id":25, "unit":"g", "order":21, "name":"Postelein", "info":"Die gelben" },
 { "recent_distribution": "2022-08-28", "id":26, "unit":"kg", "order":22, "name":"Mangold", "info":"" },
 { "recent_distribution": "2022-08-25", "id":27, "unit":"st.", "order":23, "name":"Kopfsalat", "info":"", "distributed": {
     "2022-08-03":55,
     "2022-08-05":94,
     "2022-08-08":45
   }
 },
 { "recent_distribution": "2022-08-20", "id":28, "unit":"g", "order":24, "name":"Petersilie", "info":"" },
 { "recent_distribution": "2022-08-20", "id":29, "unit":"g", "order":25, "name":"Schnittlauch", "info":"" },
 { "recent_distribution": "2022-08-20", "id":30, "unit":"kg", "order":26, "name":"Tatsoi", "info":"" },
 { "recent_distribution": "2022-08-20", "id":31, "unit":"st.", "order":27, "name":"Kohlrabi", "info":"" },
 { "recent_distribution": "2022-07-11", "id":32, "unit":"g", "order":28, "name":"Bohnenkraut", "info":"Hübsche große Bohnen" },
 { "recent_distribution": "2022-07-11", "id":33, "unit":"g", "order":29, "name":"Liebstöckel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":34, "unit":"kg", "order":30, "name":"Frühlingszwiebel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":35, "unit":"st.", "order":31, "name":"Rettich", "info":"" },
 { "recent_distribution": "2022-07-11", "id":36, "unit":"g", "order":32, "name":"Ysop", "info":"" },
 { "recent_distribution": "2022-07-11", "id":37, "unit":"g", "order":33, "name":"Koriander", "info":"" },
 { "recent_distribution": "2022-07-11", "id":38, "unit":"g", "order":34, "name":"Fenchel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":39, "unit":"kg", "order":35, "name":"Brokoli", "info":"" },
 { "recent_distribution": "2022-07-11", "id":40, "unit":"kg", "order":36, "name":"Brokkoli", "info":"" },
 { "recent_distribution": "2022-07-11", "id":41, "unit":"kg", "order":37, "name":"Stangensellerie", "info":"" },
 { "recent_distribution": "2022-07-11", "id":42, "unit":"kg", "order":38, "name":"Dickebohnen", "info":"" },
 { "recent_distribution": "2022-07-11", "id":43, "unit":"kg", "order":39, "name":"Zuckerschoten", "info":"" },
 { "recent_distribution": "2022-07-11", "id":44, "unit":"st.", "order":40, "name":"Gurken", "info":"Die grünen sind nicht giftig!" },
 { "recent_distribution": "2022-07-11", "id":45, "unit":"st.", "order":41, "name":"Zucchini", "info":"" },
 { "recent_distribution": "2022-07-11", "id":46, "unit":"g", "order":42, "name":"Basilikum", "info":"" },
 { "recent_distribution": "2022-07-11", "id":47, "unit":"g", "order":43, "name":"Knoblauch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":48, "unit":"kg", "order":44, "name":"Lauchzwiebeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":49, "unit":"st.", "order":45, "name":"Bundmöhren", "info":"" },
 { "recent_distribution": "2022-07-11", "id":50, "unit":"kg", "order":46, "name":"Buschbohnen", "info":"" },
 { "recent_distribution": "2022-07-11", "id":51, "unit":"kg", "order":47, "name":"Kartoffeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":52, "unit":"kg", "order":48, "name":"Tomaten", "info":"" },
 { "recent_distribution": "2022-07-11", "id":53, "unit":"st.", "order":49, "name":"Aubergine", "info":"" },
 { "recent_distribution": "2022-07-11", "id":54, "unit":"kg", "order":50, "name":"Ziebel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":55, "unit":"kg", "order":51, "name":"Lauch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":56, "unit":"st.", "order":52, "name":"Melonen", "info":"" },
 { "recent_distribution": "2022-07-11", "id":57, "unit":"kg", "order":53, "name":"Paprika", "info":"" },
 { "recent_distribution": "2022-07-11", "id":58, "unit":"g", "order":54, "name":"Dill", "info":"" },
 { "recent_distribution": "2022-07-11", "id":59, "unit":"st.", "order":55, "name":"Mairüben", "info":"" },
 { "recent_distribution": "2022-07-11", "id":60, "unit":"g", "order":56, "name":"Radicchio", "info":"" },
 { "recent_distribution": "2022-07-11", "id":61, "unit":"st.", "order":57, "name":"Kürbis", "info":"" },
 { "recent_distribution": "2022-07-11", "id":62, "unit":"g", "order":58, "name":"Chilli", "info":"" },
 { "recent_distribution": "2022-07-11", "id":63, "unit":"kg", "order":59, "name":"Zwiebeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":64, "unit":"st.", "order":60, "name":"Endivie", "info":"" },
 { "recent_distribution": "2022-07-11", "id":65, "unit":"st.", "order":61, "name":"Salat", "info":"" },
 { "recent_distribution": "2022-07-11", "id":66, "unit":"st.", "order":62, "name":"Blumenkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":67, "unit":"st.", "order":63, "name":"Chinakohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":68, "unit":"st.", "order":64, "name":"Spitzkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":69, "unit":"kg", "order":65, "name":"Schwarzkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":70, "unit":"st.", "order":66, "name":"Knollensellerie", "info":"" },
 { "recent_distribution": "2022-07-11", "id":71, "unit":"kg", "order":67, "name":"Weißkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":72, "unit":"st.", "order":68, "name":"Herbstrüben", "info":"" },
 { "recent_distribution": "2022-07-11", "id":73, "unit":"st.", "order":69, "name":"Pastinake", "info":"" },
 { "recent_distribution": "2022-07-11", "id":74, "unit":"st.", "order":70, "name":"Weiskohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":75, "unit":"kg", "order":71, "name":"Rotkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":76, "unit":"kg", "order":72, "name":"Lagermöhren", "info":"" },
 { "recent_distribution": "2022-07-11", "id":77, "unit":"kg", "order":73, "name":"Endiviensalat", "info":"" },
 { "recent_distribution": "2022-07-11", "id":78, "unit":"kg", "order":74, "name":"Pastinaken", "info":"" },
 { "recent_distribution": "2022-07-11", "id":79, "unit":"st.", "order":75, "name":"Superschmelz", "info":"" },
 { "recent_distribution": "2022-07-11", "id":80, "unit":"kg", "order":77, "name":"Rosenkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":81, "unit":"kg", "order":7, "name":"Grünkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":82, "unit":"kg", "order":8, "name":"Schwartze Rettisch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":83, "unit":"st.", "order":80, "name":"Kohlrabi Superschmelz", "info":"" },
 { "recent_distribution": "2022-07-11", "id":84, "unit":"kg", "order":81, "name":"Endivie oder Radicchio", "info":"" },
 { "recent_distribution": "2022-07-11", "id":85, "unit":"kg", "order":92, "name":"Rote Beete", "info":"" },
 { "recent_distribution": "2022-07-11", "id":86, "unit":"st.", "order":99, "name":"Radieschen (bund)", "info":"" },
 { "recent_distribution": "2022-07-11", "id":87, "unit":"kg", "order":100, "name":"Pak Choi", "info":"" }
 ]
```

## history

History will be an overview with detailed insights on different distributions made in the past. all information will be accessable in one way or another. this might be many data


## distribution

In the distribution site for a product ..
there should also be a "specials-tab" for example for options to not enter the amount harvested but to  let the tool say how much should be harvested
