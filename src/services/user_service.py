class UserService:
    def fetch_all_users():
        users = [
            {
                "id" : 1,
                "username" : "pedramkarimi",
                "tags" : ["a", "b", "c"],
                "fullname" : {        
                    "name" : "pedram",
                    "family" : "karimi"
                    }
            },
            {
                "id" : 2,
                "username" : "alitaghavi",
                "tags" : ["d", "e", "f"],
                "fullname" : {
                    "name" : "ali",
                    "family" : "taghavi",
                }
            },
            {
                "id" : 3,
                "username" : "sarabayat",
                "tags" : ["g", "h", "j"],
                "fullname" : {
                    "name" : "sara",
                    "family" : "bayat",
                }
            }
        ]
        return users