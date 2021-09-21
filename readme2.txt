Api : "/register"
 # it will insert a data of user into databse
 # It takes the the payload in the format json format 
 # ex : {
        "name":"Rohan",
        "password":"Rohan12345"
        }
 # response will be  : Message along with status


Api : "/addgame"
 # this api will add a new game deatils into the database
 # token is required to use this api
 # It takes the the payload in the format json format 
 # ex : {
	"title":"GTA 5",
	"platform":"PlayStation 3",
	"socre":8.2,
	"genre":"Platformer",
	"editors_choice":"Y"
}
 # response will be  : Message along with status  
                        {
                            "status": true,
                            "Message": "Game details saved successfully"
                        }

Api : "/login"
 # this api will login the user and create a token for futher use 
 # pass user name and password in the authorization (basic auth) 
 # ex : {
        "username":"Rohan",
        "password":"Rohan12345"
        }
 # response will be  : Message along with status
                        {
                            "status": true,
                            "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IlJvaGFuIiwicHVibGljX2lkIjoiMmFiY2I2ODktNzBjMy00YjM5LWE1ODAtNWE4ZGU5MzA4YTBlIn0.-3QTQY5YgbfFPnnCEGEtWKkNIcuM14x6mbiVM43yhQ8"
                        }


Api : "/searchgame"
 # token is required to use this api
 # it will search the games based on title
 # It takes the the payload in the format json format 
 # ex : {
        "title" : "GTA 5"
        }
 # response will be  : Message along with status
                        {
                            "status": true,
                            "Search result": [
                                [
                                    {
                                        "title": "GTA 5",
                                        "platform": "",
                                        "genre": "Platformer",
                                        "score": 0,
                                        "editors_choice": "Y"
                                    },
                                    {
                                        "title": "GTA 5",
                                        "platform": "PlayStation 3",
                                        "genre": "Platformer",
                                        "score": 0,
                                        "editors_choice": "Y"
                                    }
                                ]
                            ]
                        }


Api : "/filtergames"
 # this api will filter the game deatils  based on key values provided in the body
 # sort_order is 
 # token is required for using this api
 # It takes the the payload in the format json format 
 # sortortder is optional
 # ex : {	
            "title":"GTA 5",
            "sort_order":"asc"
        } 
 # response will be  : Message along with status
                        {
                            "status": true,
                            "Message": "Game Details Deleted Successfully"
                        }


Api : "/updategame"
 # this api will update the game deatils  based on id
 # token is required for using this api
 # It takes the the payload in the format json format 
 # ex : {
            "id":139,
            "title" : "GTA 3",
            "platform" : "PS 2",
            "score" : 15.06,
            "genre" : "Action",
            "editors_choice" : "N"
            
        }
 # response will be  : Message along with status
                        {
                            "status": true,
                            "Message": "Games data Updated Successfully"
                        }


Api : "/deletegame/<id>"
 # this api will delete the game deatils  based on id
 # token is required for using this api
 # It takes the the payload in the format json format 
 # id is reuired in the query params
 # response will be  : Message along with status
                        {
                            "status": true,
                            "Message": "Game Details Deleted Successfully"
                        }
                                                