

from flask import Flask
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)




# from flask import Flask
#from authors_app import create_app
#app = create_app()
#if __name__ == "__main__":
    #app =create_app()
    #app.run(debug=True) 
