# development data

this is just a quick write up with some data for different webpages as I want to try out designing some portions before taking care of the backend

## stations

Stations is a overview page of stations to deliver to. It includes some historical data of stations, a method to add a new and change existing ones.


[testmark]:# (stations-current)
```json
[
 { "id":1, "order":2, "last_edit": "2022-08-12", "info":"Kackstraße 15, marianne", "name":"Ost", "members_full":32, "members_half":15 },
 { "id":3, "order":1, "last_edit": "2022-08-9", "info":"Weit draussn beim platz", "name":"West", "members_full":12, "members_half":5 },
 { "id":4, "order":5, "last_edit": "2022-08-8", "info":"Steven, kontakt 027 // 1238 27 199", "name":"Süd", "members_full":26, "members_half":19 },
 { "id":5, "order":3, "last_edit": "2022-08-12", "info":"erna anklingeln vorher", "name":"Ost II", "members_full":2, "members_half":2 },
 { "id":6, "order":4, "last_edit": "2022-08-12", "info":"mariannenplatz 123, anrufen: 0182 / 23723 211 1", "name":"West II", "members_full":20, "members_half":8 },
 { "id":8, "order":6, "last_edit": "2022-08-12", "info":"bratwursthund 123, 04315 Leipzig", "name":"Nord", "members_full":10, "members_half":6 }
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
 { "recent_distribution": "2022-08-28", "id":20, "unit_id":2, "name":"Rucola", "info":"" },
 { "recent_distribution": "2022-08-27", "id":21, "unit_id":1, "name":"Feldsalat ", "info":"" },
 { "recent_distribution": "2022-08-26", "id":22, "unit_id":2, "name":"Porree", "info":"" },
 { "recent_distribution": "2022-08-28", "id":23, "unit_id":1, "name":"Asiasalat", "info":"" },
 { "recent_distribution": "2022-08-28", "id":24, "unit_id":1, "name":"Spinat", "info":"" },
 { "recent_distribution": "2022-08-25", "id":25, "unit_id":1, "name":"Postelein", "info":"Die gelben" },
 { "recent_distribution": "2022-08-28", "id":26, "unit_id":1, "name":"Mangold", "info":"" },
 { "recent_distribution": "2022-08-25", "id":27, "unit_id":2, "name":"Kopfsalat", "info":""},
 { "recent_distribution": "2022-08-20", "id":28, "unit_id":1, "name":"Petersilie", "info":"" },
 { "recent_distribution": "2022-08-20", "id":29, "unit_id":1, "name":"Schnittlauch", "info":"" },
 { "recent_distribution": "2022-08-20", "id":30, "unit_id":1, "name":"Tatsoi", "info":"" },
 { "recent_distribution": "2022-08-20", "id":31, "unit_id":2, "name":"Kohlrabi", "info":"" },
 { "recent_distribution": "2022-07-11", "id":32, "unit_id":1, "name":"Bohnenkraut", "info":"Hübsche große Bohnen" },
 { "recent_distribution": "2022-07-11", "id":33, "unit_id":1, "name":"Liebstöckel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":34, "unit_id":1, "name":"Frühlingszwiebel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":35, "unit_id":2, "name":"Rettich", "info":"" },
 { "recent_distribution": "2022-07-11", "id":36, "unit_id":1, "name":"Ysop", "info":"" },
 { "recent_distribution": "2022-07-11", "id":37, "unit_id":1, "name":"Koriander", "info":"" },
 { "recent_distribution": "2022-07-11", "id":38, "unit_id":1, "name":"Fenchel", "info":"" },
 { "recent_distribution": null, "id":39, "unit_id":1, "name":"Brokoli", "info":"" },
 { "recent_distribution": null, "id":40, "unit_id":1, "name":"Brokkoli", "info":"" },
 { "recent_distribution": null, "id":41, "unit_id":1, "name":"Stangensellerie", "info":"" },
 { "recent_distribution": null, "id":42, "unit_id":1, "name":"Dickebohnen", "info":"" },
 { "recent_distribution": null, "id":43, "unit_id":1, "name":"Zuckerschoten", "info":"" },
 { "recent_distribution": null, "id":44, "unit_id":2, "name":"Gurken", "info":"Die grünen sind nicht giftig!" },
 { "recent_distribution": null, "id":45, "unit_id":2, "name":"Zucchini", "info":"" },
 { "recent_distribution": null, "id":46, "unit_id":1, "name":"Basilikum", "info":"" },
 { "recent_distribution": "2022-07-11", "id":47, "unit_id":1, "name":"Knoblauch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":48, "unit_id":1, "name":"Lauchzwiebeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":49, "unit_id":2, "name":"Bundmöhren", "info":"" },
 { "recent_distribution": "2022-07-11", "id":50, "unit_id":1, "name":"Buschbohnen", "info":"" },
 { "recent_distribution": "2022-07-11", "id":51, "unit_id":1, "name":"Kartoffeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":52, "unit_id":1, "name":"Tomaten", "info":"" },
 { "recent_distribution": "2022-07-11", "id":53, "unit_id":2, "name":"Aubergine", "info":"" },
 { "recent_distribution": "2022-07-11", "id":54, "unit_id":1, "name":"Ziebel", "info":"" },
 { "recent_distribution": "2022-07-11", "id":55, "unit_id":1, "name":"Lauch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":56, "unit_id":2, "name":"Melonen", "info":"" },
 { "recent_distribution": "2022-07-11", "id":57, "unit_id":1, "name":"Paprika", "info":"" },
 { "recent_distribution": "2022-07-11", "id":58, "unit_id":1, "name":"Dill", "info":"" },
 { "recent_distribution": "2022-07-11", "id":59, "unit_id":2, "name":"Mairüben", "info":"" },
 { "recent_distribution": "2022-07-11", "id":60, "unit_id":1, "name":"Radicchio", "info":"" },
 { "recent_distribution": "2022-07-11", "id":61, "unit_id":2, "name":"Kürbis", "info":"" },
 { "recent_distribution": "2022-07-11", "id":62, "unit_id":1, "name":"Chilli", "info":"" },
 { "recent_distribution": "2022-07-11", "id":63, "unit_id":1, "name":"Zwiebeln", "info":"" },
 { "recent_distribution": "2022-07-11", "id":64, "unit_id":2, "name":"Endivie", "info":"" },
 { "recent_distribution": "2022-07-11", "id":65, "unit_id":2, "name":"Salat", "info":"" },
 { "recent_distribution": "2022-07-11", "id":66, "unit_id":2, "name":"Blumenkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":67, "unit_id":2, "name":"Chinakohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":68, "unit_id":2, "name":"Spitzkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":69, "unit_id":1, "name":"Schwarzkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":70, "unit_id":2, "name":"Knollensellerie", "info":"" },
 { "recent_distribution": "2022-07-11", "id":71, "unit_id":1, "name":"Weißkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":72, "unit_id":2, "name":"Herbstrüben", "info":"" },
 { "recent_distribution": "2022-07-11", "id":73, "unit_id":2, "name":"Pastinake", "info":"" },
 { "recent_distribution": "2022-07-11", "id":74, "unit_id":2, "name":"Weiskohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":75, "unit_id":1, "name":"Rotkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":76, "unit_id":1, "name":"Lagermöhren", "info":"" },
 { "recent_distribution": "2022-07-11", "id":77, "unit_id":1, "name":"Endiviensalat", "info":"" },
 { "recent_distribution": "2022-07-11", "id":78, "unit_id":1, "name":"Pastinaken", "info":"" },
 { "recent_distribution": "2022-07-11", "id":79, "unit_id":2, "name":"Superschmelz", "info":"" },
 { "recent_distribution": "2022-07-11", "id":80, "unit_id":1, "name":"Rosenkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":81, "unit_id":1, "name":"Grünkohl", "info":"" },
 { "recent_distribution": "2022-07-11", "id":82, "unit_id":1, "name":"Schwartze Rettisch", "info":"" },
 { "recent_distribution": "2022-07-11", "id":83, "unit_id":2, "name":"Kohlrabi Superschmelz", "info":"" },
 { "recent_distribution": "2022-07-11", "id":84, "unit_id":1, "name":"Endivie oder Radicchio", "info":"" },
 { "recent_distribution": "2022-07-11", "id":85, "unit_id":1, "name":"Rote Beete", "info":"" },
 { "recent_distribution": "2022-07-11", "id":86, "unit_id":2, "name":"Radieschen (bund)", "info":"" },
 { "recent_distribution": "2022-07-11", "id":87, "unit_id":1, "name":"Pak Choi", "info":"" }
 ]
```

## history

History will be an overview with detailed insights on different distributions made in the past. all information will be accessable in one way or another. this might be many data


## distribution

In the distribution site for a product ..
there should also be a "specials-tab" for example for options to not enter the amount harvested but to  let the tool say how much should be harvested


there should be a small menu of products already in the distribution

[testmark]:# (in-distribution)
```json
[
 { "id":31, "unit":"st.", "name":"Kohlrabi", "amount":41},
 { "id":32, "unit":"g", "name":"Bohnenkraut", "amount": 4200 },
 { "id":33, "unit":"g", "name":"Liebstöckel", "amount": 1100 },
 { "id":34, "unit":"kg", "name":"Frühlingszwiebel", "amount": 84}
]
```


## settings

The settings page is, in its base rather minimal. There we can change, add or delete values. Some Values are for example

units: they affect the frontend, how the two different units (by piece, by weight) are shown (pp. / kg.). They also affect the generation of the pdf after its generation

[testmark]:# (test-settings)
```json

{"units": [
        {"id": 5, "unit_id":1, "name":"kg"},
        {"id": 7, "unit_id":0, "name":"st."},
        {"id": 3, "unit_id":1, "name":"g"}],
 "base_units" : [{"id":0, "description": "für Erzeugnisse -in stück-"},
           {"id":1, "description": "für -in Kilo-"}],
 "logo": "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
 "csa_name": "RunkelRübeCSA",
 "packinglist_footer": "Bestes Futter seit 1923 - 🥦"}
```
