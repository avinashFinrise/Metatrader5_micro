import pickle,os,requests
from json import loads
import sys,websocket,time

class ConnectToAPI :

    """
        Class : ConnectToAPI 
        params to pass in constructor : 
            username : username provided for loggin in to rest api of rms
    
    """

    def __init__(self) :
        pass
        
       

    def dataSerializer(self,__data):
        """
            CHECKING FOR KEYS IN DATA 
        """
        
        if isinstance(__data,dict):
            try:
                self.__username = __data["username"]
                self.__password = __data["password"]
                self.__loginURL = __data["loginURL"]
                self._wsURL = __data["wsURL"]
            except KeyError as e:
                raise KeyError(str(e)+ "is missing please check")                  
        else :
            raise TypeError("Object of unsupproted type cannot be serialized")

    def _login(creds=dict()):
        print("creds: ", creds)
         # self.dataSerializer(kwargs)            
        _pickleFile = "C:/Users/JAYESH/Desktop/mt5_python/utils/session.pkl"
        # LOGGING IN TO API ENDPOINT
        # self.__login()

        __sessionData= None
        try :
            with open(_pickleFile,"rb") as file :
                __sessionData = pickle.load(file)    
        except Exception as e:
            print("while reading pickle",e)
        
        # dataSerializer(creds)            

        try:
            __body = {
                "event":"login",
                "source":"web",
                "data":{
                    "username":"gauravmeta",
                    "password":"Gaurav@123"
                }
            }
            __response = requests.post(url=creds.get('loginURL'),json=__body)
            if __response.status_code == 200 :                
                __session = Session(sessionid=__response.cookies.get("sessionid"),csrf=__response.cookies.get("csrftoken"),accesstoken=loads(__response.text).get("access_token"))
                with open(_pickleFile,"wb") as f :
                    pickle.dump(__session,f)   
                print("logged in successfully")
            else :
                print("response from api ============== ",__response.text)
                sys.exit(1)
        except Exception as e:
            print("Error while connecting to api",e)

    def connectWebSocket(creds=dict()):
        try:
            _pickleFile = "C:/Users/JAYESH/Desktop/mt5_python/utils/session.pkl"
            __sessionData= None
            try :
                with open(_pickleFile,"rb") as file :
                    __sessionData = pickle.load(file)    
            except Exception as e:
                print("while reading pickle",e)
            print(creds.get("wsURL"))
            websocket_con = websocket.create_connection(creds.get("wsURL"),cookie=f"csrftoken={__sessionData.csrf};sessionid={__sessionData.sessionid}")
            
            print("Success on connectWebSocket")
            return websocket_con
        except Exception as e:
            print("Error on connectWebSocket ",e)
    


class Session :
    """
        setter and getter class to store data in pickle file
    """

    def __init__(self,**kwargs) :
        self.__sessionid = kwargs.get("sessionid")
        self.__csrf = kwargs.get("csrf")
        self.__accesstoken = kwargs.get("accesstoken")

    @property
    def sessionid(self):
        return self.__sessionid     

    @sessionid.setter
    def sessionid(self,value):
        self.__sessionid = value

    @property
    def csrf(self):
        return self.__csrf     

    @csrf.setter
    def csrf(self,value):
        self.__csrf = value

    @property
    def accesstoken(self):
        return self.__accesstoken
    
    @accesstoken.setter
    def accesstoken(self,value):
        self.__accesstoken = value 



